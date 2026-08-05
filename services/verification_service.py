import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Profile, VerificationDecision, VerificationStatus
from repositories.trust import TrustRepository
from services.trust_score_service import TrustScoreService


class VerificationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TrustRepository(session)

    async def submit(self, user_id: int, video_file_id: str):
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        if profile is None:
            raise ValueError("Сначала создайте анкету.")
        profile.verification_status = VerificationStatus.PENDING
        return await self.repo.open_verification(user_id, video_file_id)

    async def decide(
        self, request_id: uuid.UUID, admin_id: int, decision: VerificationDecision, comment: str | None = None
    ):
        request = await self.repo.verification(request_id)
        if request is None or request.status != VerificationDecision.PENDING:
            return None, False
        request.status, request.admin_id, request.comment = decision, admin_id, comment
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == request.user_id))
        if profile:
            profile.verification_status = {
                VerificationDecision.APPROVED: VerificationStatus.VERIFIED,
                VerificationDecision.REJECTED: VerificationStatus.REJECTED,
                VerificationDecision.RETAKE_REQUESTED: VerificationStatus.UNVERIFIED,
            }[decision]
        if decision == VerificationDecision.APPROVED:
            await TrustScoreService(self.session).change(
                request.user_id, 5, "verified", reference_type="verification", reference_id=str(request.id)
            )
        await self.repo.log(
            admin_id,
            f"verification_{decision.value.lower()}",
            target_type="verification",
            target_id=str(request.id),
            details=comment,
        )
        await self.session.flush()
        return request, True
