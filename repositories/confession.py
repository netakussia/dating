import uuid
from datetime import UTC, datetime

from sqlalchemy import or_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Confession, ConfessionDailyLimit, ConfessionStatus


class ConfessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, confession: Confession) -> Confession:
        nested = getattr(self.session, "begin_nested", None)
        try:
            if nested is None:
                self.session.add(confession)
                await self.session.flush()
            else:
                async with nested():
                    self.session.add(confession)
                    await self.session.flush()
        except IntegrityError:
            if confession.submission_key:
                existing = await self.by_submission_key(confession.submission_key)
                if existing is not None:
                    return existing
            raise
        return confession

    async def by_submission_key(self, submission_key: str) -> Confession | None:
        return await self.session.scalar(
            select(Confession).where(Confession.submission_key == submission_key)
        )

    async def reserve_daily_send(self, sender_hash: str, *, limit: int) -> bool:
        """Reserve one send without a read/modify/write race between workers."""
        statement = (
            insert(ConfessionDailyLimit)
            .values(sender_hash=sender_hash, sent_count=1)
            .on_conflict_do_update(
                index_elements=[ConfessionDailyLimit.sender_hash],
                set_={"sent_count": ConfessionDailyLimit.sent_count + 1},
                where=ConfessionDailyLimit.sent_count < limit,
            )
            .returning(ConfessionDailyLimit.sender_hash)
        )
        return (await self.session.scalar(statement)) is not None

    async def get_pending(self, confession_id: uuid.UUID) -> Confession | None:
        return await self.session.scalar(
            select(Confession).where(
                Confession.id == confession_id,
                Confession.status == ConfessionStatus.PENDING,
                or_(Confession.expires_at.is_(None), Confession.expires_at > datetime.now(UTC)),
            )
        )

    async def claim_pending(self, confession_id: uuid.UUID, recipient_id: int) -> Confession | None:
        """Claim exactly once so repeated /start updates cannot redeliver it."""
        result = await self.session.execute(
            update(Confession)
            .where(
                Confession.id == confession_id,
                Confession.status == ConfessionStatus.PENDING,
                or_(Confession.expires_at.is_(None), Confession.expires_at > datetime.now(UTC)),
            )
            .values(recipient_id=recipient_id, status=ConfessionStatus.DELIVERED)
            .returning(Confession)
        )
        return result.scalar_one_or_none()
