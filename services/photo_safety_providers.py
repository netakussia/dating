from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class PhotoSafetyConfigurationError(RuntimeError):
    pass


class PhotoSafetyProviderError(RuntimeError):
    """Inference failed after the image passed input validation.

    Callers treat this as a fail-soft signal, rather than as a user error.
    """

    pass


@dataclass(frozen=True, slots=True)
class SafeImage:
    """Decoded, EXIF-stripped image accepted by the moderation boundary."""

    rgb_bytes: bytes
    width: int
    height: int


@dataclass(frozen=True, slots=True)
class PhotoAssessment:
    nsfw_score: float
    face_detected: bool
    provider: str = "heuristic"
    face_score: float = 1.0
    face_count: int = 1
    human_score: float = 1.0
    fallback_reason: str | None = None


class PhotoSafetyProvider(Protocol):
    name: str

    async def assess(self, image: SafeImage | None) -> PhotoAssessment: ...


class HeuristicPhotoSafetyProvider:
    name = "heuristic"

    async def assess(self, image: SafeImage | None) -> PhotoAssessment:
        return PhotoAssessment(nsfw_score=0.0, face_detected=True, provider=self.name)


class DisabledPhotoSafetyProvider:
    name = "disabled"

    async def assess(self, image: SafeImage | None) -> PhotoAssessment:
        return PhotoAssessment(nsfw_score=0.0, face_detected=True, provider=self.name)


def face_detection_size(width: int, height: int, max_dimension: int) -> tuple[int, int]:
    """Fit a camera image into YuNet's working size without distorting it."""
    largest_dimension = max(width, height)
    if largest_dimension <= max_dimension:
        return width, height
    scale = max_dimension / largest_dimension
    return max(1, round(width * scale)), max(1, round(height * scale))


class OnnxPhotoSafetyProvider:
    """Local CPU inference: OpenNSFW-compatible ONNX + OpenCV YuNet, no cloud calls."""

    name = "ml_onnx"

    def __init__(
        self,
        *,
        nsfw_model_path: str,
        face_model_path: str,
        face_threshold: float,
        face_max_dimension: int,
        person_model_path: str | None = None,
        inference_timeout_seconds: float = 12.0,
    ) -> None:
        self.nsfw_model_path = Path(nsfw_model_path)
        self.face_model_path = Path(face_model_path)
        self.face_threshold = face_threshold
        self.face_max_dimension = face_max_dimension
        self.person_model_path = Path(person_model_path) if person_model_path else None
        self.inference_timeout_seconds = inference_timeout_seconds
        self._nsfw_session = None
        self._person_session = None

    async def assess(self, image: SafeImage | None) -> PhotoAssessment:
        if image is None:
            raise PhotoSafetyProviderError("Telegram photo source is required for ML provider")
        try:
            return await asyncio.wait_for(
                asyncio.to_thread(self._assess_sync, image), timeout=self.inference_timeout_seconds
            )
        except TimeoutError as error:
            raise PhotoSafetyProviderError("ML inference timed out") from error

    def _assess_sync(self, image: SafeImage) -> PhotoAssessment:
        if not self.nsfw_model_path.is_file() or not self.face_model_path.is_file():
            raise PhotoSafetyProviderError("Local ONNX models are missing")
        try:
            import cv2
            import numpy as np
            import onnxruntime as ort
        except ImportError as error:  # pragma: no cover - covered by deployment image
            raise PhotoSafetyProviderError("ML dependencies are not installed") from error

        try:
            return self._run_cascade(cv2, np, ort, image)
        except Exception as error:  # ONNXRuntimeError differs between installed ORT versions.
            raise PhotoSafetyProviderError(f"{type(error).__name__}: {error}") from error

    def _run_cascade(self, cv2, np, ort, image: SafeImage) -> PhotoAssessment:

        decoded = cv2.imdecode(np.frombuffer(image.rgb_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        if decoded is None:
            raise ValueError("Normalized image cannot be decoded")
        face_width, face_height = face_detection_size(image.width, image.height, self.face_max_dimension)
        face_image = decoded
        if (face_width, face_height) != (image.width, image.height):
            face_image = cv2.resize(decoded, (face_width, face_height), interpolation=cv2.INTER_AREA)
        detector = cv2.FaceDetectorYN.create(
            str(self.face_model_path), "", (face_width, face_height), self.face_threshold, 0.3, 5000
        )
        _, faces = detector.detect(face_image)
        face_rows = [] if faces is None else faces
        face_count = len(face_rows)
        face_scores = [float(row[-1]) for row in face_rows]
        face_score = max(face_scores, default=0.0)

        # The primary detector has made a conclusive decision. Do not let a
        # later optional model outage turn a cat/object/meme into Yellow.
        if face_count == 0:
            return PhotoAssessment(
                nsfw_score=0.0,
                face_detected=False,
                provider=self.name,
                face_score=0.0,
                face_count=0,
                human_score=0.0,
            )

        if self._nsfw_session is None:
            self._nsfw_session = ort.InferenceSession(str(self.nsfw_model_path), providers=["CPUExecutionProvider"])
        model_input = self._nsfw_session.get_inputs()[0]
        resized = cv2.resize(decoded, (224, 224), interpolation=cv2.INTER_AREA).astype(np.float32)
        if model_input.shape[-1] == 3:
            # Keras/OpenNSFW2 ONNX exports use NHWC RGB tensors.
            tensor = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)[None, ...]
        else:
            # Legacy Yahoo/OpenNSFW exports use BGR NCHW with Caffe channel means.
            resized -= np.array([104.0, 117.0, 123.0], dtype=np.float32)
            tensor = np.transpose(resized, (2, 0, 1))[None, ...]
        input_name = model_input.name
        output = np.asarray(self._nsfw_session.run(None, {input_name: tensor})[0]).reshape(-1)
        if output.size < 2:
            raise ValueError("OpenNSFW model returned an invalid output")
        score = float(output[-1])
        if not 0.0 <= score <= 1.0:
            raise ValueError("OpenNSFW model returned an invalid score")
        # SCRFD is a second, independent ONNX face detector. Agreement between
        # YuNet and SCRFD is used as a conservative real-person/liveness proxy:
        # artwork and memes often produce a weak or no SCRFD detection. It is not
        # biometric identification and no embeddings are stored.
        human_score = face_score
        if self.person_model_path and self.person_model_path.is_file():
            if self._person_session is None:
                self._person_session = ort.InferenceSession(
                    str(self.person_model_path), providers=["CPUExecutionProvider"]
                )
            person_input = self._person_session.get_inputs()[0]
            input_h, input_w = person_input.shape[2:4]
            # SCRFD exports commonly expose dynamic H/W. This 2.5G export has
            # 6400 score anchors at stride 8, i.e. its intended 640x640 input.
            input_h = int(input_h) if isinstance(input_h, int) else 640
            input_w = int(input_w) if isinstance(input_w, int) else 640
            person_image = cv2.resize(decoded, (input_w, input_h)).astype(np.float32)
            person_image = (person_image - 127.5) / 128.0
            person_tensor = np.transpose(person_image, (2, 0, 1))[None, ...]
            outputs = self._person_session.run(None, {person_input.name: person_tensor})
            scores = [
                float(np.max(values))
                for output in outputs
                if (values := np.asarray(output)).size and values.ndim == 2 and values.shape[-1] == 1
            ]
            # Detector score is a validation signal only; retain YuNet score when
            # model output layout cannot be interpreted safely.
            if scores:
                human_score = min(face_score, max(scores))
        return PhotoAssessment(
            nsfw_score=score,
            face_detected=face_count > 0,
            provider=self.name,
            face_score=face_score,
            face_count=face_count,
            human_score=human_score,
        )


_PROVIDER_CACHE: dict[tuple[str, str, str, str, float, int, float], PhotoSafetyProvider] = {}


def build_photo_safety_provider(settings) -> PhotoSafetyProvider:
    if settings.photo_safety_provider == "heuristic":
        return HeuristicPhotoSafetyProvider()
    if settings.photo_safety_provider == "disabled":
        return DisabledPhotoSafetyProvider()
    if settings.photo_safety_provider == "ml":
        return OnnxPhotoSafetyProvider(
            nsfw_model_path=settings.nsfw_model_path,
            face_model_path=settings.face_model_path,
            face_threshold=settings.face_detection_threshold,
            face_max_dimension=settings.face_detection_max_dimension,
            person_model_path=getattr(settings, "person_model_path", None),
            inference_timeout_seconds=getattr(settings, "photo_safety_inference_timeout_seconds", 12.0),
        )
    raise PhotoSafetyConfigurationError(f"Unknown photo safety provider: {settings.photo_safety_provider}")


def get_photo_safety_provider(settings) -> PhotoSafetyProvider:
    """Reuse loaded model sessions for the bot process; selection still comes entirely from config."""
    key = (
        settings.photo_safety_provider,
        settings.nsfw_model_path,
        settings.face_model_path,
        getattr(settings, "person_model_path", ""),
        settings.face_detection_threshold,
        settings.face_detection_max_dimension,
        getattr(settings, "photo_safety_inference_timeout_seconds", 12.0),
    )
    if key not in _PROVIDER_CACHE:
        _PROVIDER_CACHE[key] = build_photo_safety_provider(settings)
    return _PROVIDER_CACHE[key]
