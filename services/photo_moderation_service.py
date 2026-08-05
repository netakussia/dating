from dataclasses import dataclass
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import ModerationCaseType, ModerationStatus, Profile
from repositories.trust import TrustRepository


@dataclass(frozen=True, slots=True)
class PhotoAssessment:
    nsfw_score: float
    face_detected: bool
    provider: str = "heuristic"


class PhotoSafetyProvider(Protocol):
    async def assess(self, photo_file_id: str) -> PhotoAssessment: ...


class HeuristicPhotoSafetyProvider:
    """Safe dependency-free default. Replace through PhotoModerationService(provider=...)."""

    async def assess(self, photo_file_id: str) -> PhotoAssessment:
        return PhotoAssessment(nsfw_score=0.0, face_detected=True)


class PhotoModerationService:
    def __init__(
        self, session: AsyncSession, *, nsfw_threshold: float, provider: PhotoSafetyProvider | None = None
    ) -> None:
        self.session, self.threshold = session, nsfw_threshold
        self.provider = provider or HeuristicPhotoSafetyProvider()
        self.repo = TrustRepository(session)

    async def inspect(self, user_id: int, photo_file_id: str) -> PhotoAssessment:
        assessment = await self.provider.assess(photo_file_id)
        await self.repo.record_photo(
            user_id, photo_file_id, assessment.provider, assessment.nsfw_score, assessment.face_detected
        )
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        is_nsfw = assessment.nsfw_score >= self.threshold
        if is_nsfw or not assessment.face_detected:
            if profile:
                profile.moderation_status = ModerationStatus.UNDER_REVIEW
                # Potentially explicit content must not remain discoverable until manual review.
                if is_nsfw:
                    profile.is_visible = False
                    profile.moderation_locked = True
            case_type = ModerationCaseType.NSFW if is_nsfw else ModerationCaseType.NO_FACE
            await self.repo.open_case(
                user_id,
                case_type,
                source_id=photo_file_id,
                details=f"score={assessment.nsfw_score:.3f}; face={assessment.face_detected}",
            )
        return assessment
