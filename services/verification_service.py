import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Profile, VerificationDecision, VerificationRequest, VerificationStatus
from repositories.trust import TrustRepository
from services.trust_score_service import TrustScoreService


class VerificationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TrustRepository(session)

    async def submit(self, user_id: int, video_file_id: str):
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id).with_for_update())
        if profile is None:
            raise ValueError("Сначала создайте анкету.")
        if profile.verification_status == VerificationStatus.VERIFIED:
            raise ValueError("Вы уже верифицированы и повторная отправка кружка недоступна.")
        if profile.verification_status == VerificationStatus.PENDING:
            raise ValueError("У вас уже есть текущая заявка на верификацию.")
        active = await self.repo.active_verification_for_user(user_id)
        if active is not None:
            raise ValueError("У вас уже есть активная заявка на верификацию.")
        profile.verification_status = VerificationStatus.PENDING
        request, _ = await self.repo.open_verification(user_id, video_file_id)
        return request

    async def claim(self, request_id: uuid.UUID, admin_id: int) -> VerificationRequest | None:
        """Claim a verification request for processing."""
        from datetime import datetime, timezone
        result = await self.session.execute(
            update(VerificationRequest)
            .where(
                VerificationRequest.id == request_id,
                VerificationRequest.status == VerificationDecision.PENDING,
                (VerificationRequest.assigned_to.is_(None) | (VerificationRequest.assigned_to == admin_id)),
            )
            .values(assigned_to=admin_id, assigned_at=datetime.now(timezone.utc))
            .returning(VerificationRequest)
        )
        request = result.scalar_one_or_none()
        if request is not None:
            return request
        current = await self.repo.verification(request_id)
        if current is None or current.status != VerificationDecision.PENDING:
            return None
        if current.assigned_to not in {None, admin_id}:
            return None
        current.assigned_to = admin_id
        current.assigned_at = datetime.now(timezone.utc)
        await self.session.flush()
        return current

    async def decide(
        self, request_id: uuid.UUID, admin_id: int, decision: VerificationDecision, comment: str | None = None
    ):
        result = await self.session.execute(
            update(VerificationRequest)
            .where(VerificationRequest.id == request_id, VerificationRequest.status == VerificationDecision.PENDING)
            .values(status=decision, admin_id=admin_id, comment=comment)
            .returning(VerificationRequest)
        )
        request = result.scalar_one_or_none()
        if request is None:
            return None, False
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
