import io
from types import SimpleNamespace

import pytest
from PIL import Image

from config import Settings
from services.photo_moderation_service import (
    PhotoAssessment,
    PhotoModerationService,
    PhotoValidationError,
    normalize_image,
)
from services.photo_safety_providers import (
    DisabledPhotoSafetyProvider,
    HeuristicPhotoSafetyProvider,
    OnnxPhotoSafetyProvider,
    build_photo_safety_provider,
    face_detection_size,
)


def safety_settings(**changes):
    values = {
        "photo_safety_provider": "heuristic",
        "nsfw_model_path": "/missing/nsfw.onnx",
        "face_model_path": "/missing/face.onnx",
        "face_detection_threshold": 0.75,
        "face_detection_max_dimension": 960,
        "photo_safety_min_dimension": 64,
        "photo_safety_max_pixels": 1_000_000,
    }
    values.update(changes)
    return SimpleNamespace(**values)


def test_photo_safety_default_is_fail_closed():
    settings = Settings(_env_file=None, bot_token="x" * 30, daily_secret_salt="y" * 20)

    assert settings.photo_safety_provider == "ml"


def test_production_rejects_non_ml_photo_safety_provider():
    with pytest.raises(ValueError, match="PHOTO_SAFETY_PROVIDER"):
        Settings(
            _env_file=None,
            bot_token="x" * 30,
            daily_secret_salt="y" * 20,
            environment="production",
            photo_safety_provider="heuristic",
        )


def image_bytes(size=(100, 100), image_format="JPEG"):
    buffer = io.BytesIO()
    Image.new("RGB", size, "white").save(buffer, format=image_format)
    return buffer.getvalue()


def test_provider_is_selected_only_by_configuration():
    assert isinstance(build_photo_safety_provider(safety_settings()), HeuristicPhotoSafetyProvider)
    assert isinstance(
        build_photo_safety_provider(safety_settings(photo_safety_provider="disabled")), DisabledPhotoSafetyProvider
    )
    assert isinstance(build_photo_safety_provider(safety_settings(photo_safety_provider="ml")), OnnxPhotoSafetyProvider)


def test_face_detection_size_downscales_phone_photos_without_distortion():
    assert face_detection_size(3888, 5184, 960) == (720, 960)
    assert face_detection_size(709, 945, 960) == (709, 945)


def test_normalization_strips_metadata_and_produces_stable_image():
    image = normalize_image(image_bytes(), safety_settings())

    assert image.width == 100
    assert image.height == 100
    assert image.rgb_bytes.startswith(b"\xff\xd8")


@pytest.mark.parametrize("payload", [b"", b"not-an-image", image_bytes((16, 16))])
def test_invalid_or_too_small_images_are_rejected(payload):
    with pytest.raises(PhotoValidationError):
        normalize_image(payload, safety_settings())


class FakeBot:
    def __init__(self, raw):
        self.raw = raw

    async def get_file(self, _file_id):
        return SimpleNamespace(file_size=len(self.raw), file_path="photo")

    async def download_file(self, _path, destination):
        destination.write(self.raw)


class CountingProvider:
    name = "counting"

    def __init__(self):
        self.calls = 0

    async def assess(self, _image):
        self.calls += 1
        return PhotoAssessment(0.1, True, self.name)


class FakePhotoRepository:
    def __init__(self):
        self.cached = None
        self.records = []

    async def photo_by_hash(self, _content_hash):
        return self.cached

    async def record_photo(self, _user_id, _file_id, provider, score, face, content_hash):
        item = SimpleNamespace(provider=provider, nsfw_score=score, face_detected=face, content_hash=content_hash)
        self.records.append(item)
        self.cached = item
        return item

    async def open_case(self, *_args, **_kwargs):
        return None, True


class FakeSession:
    async def scalar(self, _query):
        return SimpleNamespace(moderation_status=None, is_visible=True, moderation_locked=False)


@pytest.mark.asyncio
async def test_identical_normalized_photo_reuses_saved_assessment():
    provider = CountingProvider()
    service = PhotoModerationService(
        FakeSession(),
        nsfw_threshold=0.85,
        provider=provider,
        settings=safety_settings(photo_safety_max_bytes=1_000_000),
        bot=FakeBot(image_bytes()),
    )
    service.repo = FakePhotoRepository()

    await service.inspect(1, "first")
    cached = await service.inspect(2, "second")

    assert provider.calls == 1
    assert cached.provider == "counting:cached"
