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
    PhotoSafetyProviderError,
    SafeImage,
    get_photo_safety_provider,
)

logger = logging.getLogger(__name__)


class PhotoModerationError(RuntimeError):
    pass


class PhotoValidationError(PhotoModerationError):
    pass


GREEN = "GREEN"
YELLOW = "YELLOW"
RED = "RED"


def moderation_zone(assessment: PhotoAssessment, *, nsfw_red_threshold: float = 0.85) -> str:
    """Traffic-light policy following the requested fail-soft cascade.

    The real-human score is the liveness signal, while the fallback flag is the
    advisory escape hatch: it keeps the profile visible but creates a moderation
    case instead of blocking the user.
    
    Policy:
    - RED: clear signs of problematic content (high NSFW, no face, multiple faces)
    - YELLOW: uncertain cases (low face quality, ML fallback, borderline NSFW)
    - GREEN: excellent portraits with high confidence across all signals
    """
    if assessment.fallback_reason:
        return YELLOW
    
    # Hard RED cases: high NSFW or multiple faces
    if assessment.nsfw_score >= nsfw_red_threshold or assessment.face_count > 1:
        return RED
    
    # No face detected
    if not assessment.face_detected:
        # A dating profile without a face cannot be accepted as a portrait.
        return RED
    
    # A strong face detector result plus clean NSFW is sufficient for a clear
    # portrait. The secondary human signal is only a tie-breaker for weaker
    # face detections; it is not calibrated as a human probability.
    if assessment.face_score > 0.80 and assessment.nsfw_score < 0.20:
        return GREEN

    # A weak face detector score is a hard failure. A disagreement with the
    # secondary human signal is uncertain and belongs in manual review.
    if assessment.face_score < 0.50:
        return RED
    if assessment.human_score < 0.35:
        return YELLOW
    
    # Everything else: borderline case
    return YELLOW


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

    async def inspect(
        self, user_id: int, photo_file_id: str, *, defer_no_face_review: bool = False
    ) -> PhotoAssessment:
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
                # Rows created before cascade signals were persisted cannot be
                # safely classified from nsfw_score/face_detected alone.
                if cached is not None and getattr(cached, "face_count", 0) > 0:
                    assessment = PhotoAssessment(
                        cached.nsfw_score,
                        cached.face_detected,
                        f"{cached.provider}:cached",
                        face_score=getattr(cached, "face_score", 0.0),
                        face_count=getattr(cached, "face_count", 0),
                        human_score=getattr(cached, "human_score", 0.0),
                        fallback_reason=getattr(cached, "fallback_reason", None),
                    )
                    await self._apply_assessment(
                        user_id, photo_file_id, content_hash, assessment, defer_no_face_review=defer_no_face_review
                    )
                    return assessment
            assessment = await self.provider.assess(image)
            if not 0.0 <= assessment.nsfw_score <= 1.0:
                raise ValueError("NSFW score must be between 0 and 1")
        except PhotoSafetyProviderError as error:
            # ML is advisory when unavailable: keep the profile usable, capture a
            # review case, and never turn an outage into a user-facing rejection.
            logger.warning("Photo safety provider fallback for user %s: %s (%s)", user_id, type(error).__name__, error)
            assessment = PhotoAssessment(
                nsfw_score=0.0,
                face_detected=True,
                provider="ml_provider_fallback",
                face_score=0.60,
                face_count=1,
                human_score=0.60,
                fallback_reason="ML_PROVIDER_FALLBACK",
            )
        except Exception as error:
            # Fetch/normalization failures arrive before a SafeImage exists. Any
            # later exception is provider-side (including ORT's version-specific
            # exception classes) and is deliberately fail-soft.
            if image is None and self.bot is not None:
                logger.warning("Photo input validation failed for user %s: %s", user_id, type(error).__name__)
                raise PhotoModerationError("Photo safety check failed") from error
            logger.warning("Photo safety provider fallback for user %s: %s (%s)", user_id, type(error).__name__, error)
            assessment = PhotoAssessment(
                nsfw_score=0.0,
                face_detected=True,
                provider="ml_provider_fallback",
                face_score=0.60,
                face_count=1,
                human_score=0.60,
                fallback_reason="ML_PROVIDER_FALLBACK",
            )
        await self._apply_assessment(
            user_id, photo_file_id, content_hash, assessment, defer_no_face_review=defer_no_face_review
        )
        return assessment

    async def _apply_assessment(
        self,
        user_id: int,
        photo_file_id: str,
        content_hash: str | None,
        assessment: PhotoAssessment,
        *,
        defer_no_face_review: bool = False,
    ) -> None:
        await self.repo.record_photo(
            user_id,
            photo_file_id,
            assessment.provider,
            assessment.nsfw_score,
            assessment.face_detected,
            content_hash,
            assessment.face_score,
            assessment.face_count,
            assessment.human_score,
            assessment.fallback_reason,
        )
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        zone = moderation_zone(assessment, nsfw_red_threshold=self.threshold)
        if zone == RED and defer_no_face_review:
            return
        if zone == RED:
            if profile:
                profile.moderation_status = ModerationStatus.UNDER_REVIEW
                profile.is_visible = False
                profile.moderation_locked = True
            case_type = (
                ModerationCaseType.NSFW
                if assessment.nsfw_score >= self.threshold
                else ModerationCaseType.NO_FACE
                if not assessment.face_detected
                else ModerationCaseType.PHOTO_RETAKE
            )
            case, _ = await self.repo.open_case(
                user_id,
                case_type,
                source_id=content_hash or photo_file_id,
                details=(
                    self._details(assessment, zone)
                ),
            )
            if self.bot is not None:
                await InternalNotificationService(self.bot, self.settings).send_moderation_event(
                    "⚠️ ML moderation trigger",
                    user_id=user_id,
                    reason=case_type.value,
                    case_id=str(case.id),
                    target_callback=f"mycase:case:{case.id}",
                    details=(
                        self._details(assessment, zone)
                    ),
                )
        elif zone == YELLOW:
            if profile and not profile.moderation_locked:
                profile.moderation_status = ModerationStatus.CLEAR
                profile.is_visible = True
                profile.moderation_locked = False
            case_type = (
                ModerationCaseType.ML_PROVIDER_FALLBACK
                if assessment.fallback_reason
                else ModerationCaseType.PHOTO_RETAKE
            )
            await self.repo.open_case(
                user_id, case_type, source_id=content_hash or photo_file_id, details=self._details(assessment, zone)
            )
        else:
            close_photo_cases = getattr(self.repo, "close_photo_cases", None)
            if close_photo_cases is not None:
                await close_photo_cases(user_id)
            if profile:
                # A fresh successful moderation pass is the authoritative signal that
                # the user has replaced a rejected photo. The previous auto-review lock
                # is stale once the new image is accepted, so unlock it and restore
                # visibility. If a real moderator freeze exists elsewhere, it is still
                # represented by a separate flow and can be handled independently.
                if profile.moderation_locked and profile.moderation_status == ModerationStatus.UNDER_REVIEW:
                    profile.moderation_status = ModerationStatus.CLEAR
                    profile.is_visible = True
                    profile.moderation_locked = False
                    return
                if profile.moderation_locked:
                    # Freeze/lock is a moderator-controlled state. A successful photo check
                    # must never automatically lift a moderation restriction.
                    return
                profile.moderation_status = ModerationStatus.CLEAR
                profile.is_visible = True
                profile.moderation_locked = False

    @staticmethod
    def _details(assessment: PhotoAssessment, zone: str) -> str:
        return (
            f"zone={zone}; provider={assessment.provider}; nsfw={assessment.nsfw_score:.3f}; "
            f"face_score={assessment.face_score:.3f}; face_count={assessment.face_count}; "
            f"human_score={assessment.human_score:.3f}; reason={assessment.fallback_reason or '-'}"
        )

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
