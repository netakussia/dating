from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import TrustScoreEvent, User
from repositories.trust import TrustRepository


class TrustScoreService:
    """Internal reputation ledger. Every applied change is recorded for future fraud models."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TrustRepository(session)

    async def change(
        self,
        user_id: int,
        delta: int,
        reason: str,
        *,
        reference_type: str | None = None,
        reference_id: str | None = None,
    ) -> bool:
        user = await self.session.get(User, user_id)
        if user is None:
            return False
        # A reference makes moderation retries idempotent.
        if reference_id:
            duplicate = await self.session.scalar(
                select(TrustScoreEvent).where(
                    TrustScoreEvent.user_id == user_id,
                    TrustScoreEvent.reason == reason,
                    TrustScoreEvent.reference_type == reference_type,
                    TrustScoreEvent.reference_id == reference_id,
                )
            )
            if duplicate:
                return False
        user.trust_score = max(0, min(100, user.trust_score + delta))
        await self.repo.add_score_event(user_id, delta, reason, reference_type, reference_id)
        return True
