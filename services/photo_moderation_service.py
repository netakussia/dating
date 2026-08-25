from __future__ import annotations

import hashlib
import io
import logging
import warnings

from aiogram import Bot
from PIL import Image, ImageOps, UnidentifiedImageError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings, get_settings
from models import ModerationCaseType, ModerationStatus, Profile
from repositories.trust import TrustRepository
from services.notification_service import InternalNotificationService
from services.photo_safety_providers import (
    PhotoAssessment,
    PhotoSafetyProvider,
    SafeImage,
    get_photo_safety_provider,
)

logger = logging.getLogger(__name__)


class PhotoModerationError(RuntimeError):
    pass


class PhotoValidationError(PhotoModerationError):
    pass


class TelegramPhotoSource:
    """Fetches only Telegram files and rejects oversized inputs before decoding."""

    def __init__(self, bot: Bot, *, max_bytes: int) -> None:
        self.bot = bot
        self.max_bytes = max_bytes

    async def fetch(self, photo_file_id: str) -> bytes:
        file = await self.bot.get_file(photo_file_id)
        if file.file_size is not None and file.file_size > self.max_bytes:
            raise PhotoValidationError("Photo is too large")
        destination = io.BytesIO()
        await self.bot.download_file(file.file_path, destination=destination)
        payload = destination.getvalue()
        if not payload or len(payload) > self.max_bytes:
            raise PhotoValidationError("Photo is empty or too large")
        return payload


def normalize_image(raw: bytes, settings: Settings) -> SafeImage:
    """Decode bytes instead of trusting MIME/extension; strip EXIF before ML and hashing."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(raw)) as source:
                source.verify()
            with Image.open(io.BytesIO(raw)) as source:
                if source.format not in {"JPEG", "PNG", "WEBP"}:
                    raise PhotoValidationError("Unsupported image format")
                image = ImageOps.exif_transpose(source)
                width, height = image.size
                if min(width, height) < settings.photo_safety_min_dimension:
                    raise PhotoValidationError("Photo is too small")
                if width * height > settings.photo_safety_max_pixels:
                    raise PhotoValidationError("Photo has too many pixels")
                normalized = io.BytesIO()
                image.convert("RGB").save(normalized, format="JPEG", quality=95, optimize=True)
    except (Image.DecompressionBombError, UnidentifiedImageError, OSError, ValueError) as error:
        raise PhotoValidationError("Image is damaged or unsupported") from error
    return SafeImage(rgb_bytes=normalized.getvalue(), width=width, height=height)


class PhotoModerationService:
    def __init__(
        self,
        session: AsyncSession,
        *,
        nsfw_threshold: float,
        provider: PhotoSafetyProvider | None = None,
        settings: Settings | None = None,
        bot: Bot | None = None,
    ) -> None:
        self.session, self.threshold = session, nsfw_threshold
        self.settings = settings
        self.provider = provider or get_photo_safety_provider(settings or get_settings())
        self.bot = bot
        self.repo = TrustRepository(session)

    async def inspect(self, user_id: int, photo_file_id: str) -> PhotoAssessment:
        content_hash: str | None = None
        image: SafeImage | None = None
        try:
            if self.bot is not None:
                settings = self.settings or get_settings()
                source = TelegramPhotoSource(self.bot, max_bytes=settings.photo_safety_max_bytes)
                raw = await source.fetch(photo_file_id)
                image = normalize_image(raw, settings)
                content_hash = hashlib.sha256(image.rgb_bytes).hexdigest()
                cached = await self.repo.photo_by_hash(content_hash)
                if cached is not None:
                    assessment = PhotoAssessment(cached.nsfw_score, cached.face_detected, f"{cached.provider}:cached")
                    await self._apply_assessment(user_id, photo_file_id, content_hash, assessment)
                    return assessment
            assessment = await self.provider.assess(image)
            if not 0.0 <= assessment.nsfw_score <= 1.0:
                raise ValueError("NSFW score must be between 0 and 1")
        except Exception as error:
            logger.warning("Photo safety check failed for user %s: %s", user_id, type(error).__name__)
            await self._send_to_manual_review(user_id, photo_file_id, content_hash, type(error).__name__)
            raise PhotoModerationError("Photo safety check failed") from error
        await self._apply_assessment(user_id, photo_file_id, content_hash, assessment)
        return assessment

    async def _apply_assessment(
        self, user_id: int, photo_file_id: str, content_hash: str | None, assessment: PhotoAssessment
    ) -> None:
        await self.repo.record_photo(
            user_id, photo_file_id, assessment.provider, assessment.nsfw_score, assessment.face_detected, content_hash
        )
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        is_nsfw = assessment.nsfw_score >= self.threshold
        if is_nsfw or not assessment.face_detected:
            if profile:
                profile.moderation_status = ModerationStatus.UNDER_REVIEW
                profile.is_visible = False
                profile.moderation_locked = True
            case_type = ModerationCaseType.NSFW if is_nsfw else ModerationCaseType.NO_FACE
            case, _ = await self.repo.open_case(
                user_id,
                case_type,
                source_id=content_hash or photo_file_id,
                details=(
                    f"provider={assessment.provider}; score={assessment.nsfw_score:.3f}; "
                    f"face={assessment.face_detected}"
                ),
            )
            if self.bot is not None:
                await InternalNotificationService(self.bot, self.settings).send_moderation_event(
                    "⚠️ ML moderation trigger",
                    user_id=user_id,
                    reason=case_type.value,
                    case_id=str(case.id),
                    details=(
                        f"provider={assessment.provider}; score={assessment.nsfw_score:.3f}; "
                        f"face_detected={assessment.face_detected}"
                    ),
                )
        elif profile and profile.moderation_locked:
            # Freeze/lock is a moderator-controlled state. A successful photo check
            # must never automatically lift a moderation restriction.
            return

    async def _send_to_manual_review(
        self, user_id: int, photo_file_id: str, content_hash: str | None, error_name: str
    ) -> None:
        await self.repo.record_photo(user_id, photo_file_id, "provider_error", 0.0, False, content_hash)
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        if profile:
            profile.moderation_status = ModerationStatus.UNDER_REVIEW
            profile.is_visible = False
            profile.moderation_locked = True
        await self.repo.open_case(
            user_id,
            ModerationCaseType.NSFW,
            source_id=content_hash or photo_file_id,
            details=f"provider_error={error_name}",
        )
