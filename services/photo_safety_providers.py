from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class PhotoSafetyConfigurationError(RuntimeError):
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
    ) -> None:
        self.nsfw_model_path = Path(nsfw_model_path)
        self.face_model_path = Path(face_model_path)
        self.face_threshold = face_threshold
        self.face_max_dimension = face_max_dimension
        self._nsfw_session = None

    async def assess(self, image: SafeImage | None) -> PhotoAssessment:
        if image is None:
            raise PhotoSafetyConfigurationError("Telegram photo source is required for ML provider")
        return await asyncio.to_thread(self._assess_sync, image)

    def _assess_sync(self, image: SafeImage) -> PhotoAssessment:
        if not self.nsfw_model_path.is_file() or not self.face_model_path.is_file():
            raise PhotoSafetyConfigurationError("Local ONNX models are missing")
        try:
            import cv2
            import numpy as np
            import onnxruntime as ort
        except ImportError as error:  # pragma: no cover - covered by deployment image
            raise PhotoSafetyConfigurationError("ML dependencies are not installed") from error

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
        return PhotoAssessment(nsfw_score=score, face_detected=faces is not None and len(faces) > 0, provider=self.name)


_PROVIDER_CACHE: dict[tuple[str, str, str, float, int], PhotoSafetyProvider] = {}


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
        )
    raise PhotoSafetyConfigurationError(f"Unknown photo safety provider: {settings.photo_safety_provider}")


def get_photo_safety_provider(settings) -> PhotoSafetyProvider:
    """Reuse loaded model sessions for the bot process; selection still comes entirely from config."""
    key = (
        settings.photo_safety_provider,
        settings.nsfw_model_path,
        settings.face_model_path,
        settings.face_detection_threshold,
        settings.face_detection_max_dimension,
    )
    if key not in _PROVIDER_CACHE:
        _PROVIDER_CACHE[key] = build_photo_safety_provider(settings)
    return _PROVIDER_CACHE[key]
