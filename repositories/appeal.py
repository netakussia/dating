import uuid

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Appeal, AppealStatus


class AppealRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: int, text: str) -> Appeal:
        appeal = Appeal(user_id=user_id, text=text)
        try:
            nested = getattr(self.session, "begin_nested", None)
            if nested is None:
                self.session.add(appeal)
                await self.session.flush()
            else:
                async with nested():
                    self.session.add(appeal)
                    await self.session.flush()
        except IntegrityError:
            existing = await self.active_for_user(user_id)
            if existing is not None:
                return existing
            raise
        return appeal

    async def get(self, appeal_id: uuid.UUID) -> Appeal | None:
        return await self.session.get(Appeal, appeal_id)

    async def active_for_user(self, user_id: int) -> Appeal | None:
        statement = (
            select(Appeal)
            .where(Appeal.user_id == user_id, Appeal.status == AppealStatus.PENDING)
            .order_by(Appeal.created_at.desc())
        )
        return await self.session.scalar(statement)

    async def pending(self, moderator_id: int | None = None) -> list[Appeal]:
        statement = select(Appeal).where(Appeal.status == AppealStatus.PENDING)
        if moderator_id is not None:
            statement = statement.where((Appeal.assigned_to == moderator_id) | (Appeal.assigned_to.is_(None)))
        statement = statement.order_by(Appeal.created_at)
        return list((await self.session.scalars(statement)).all())

    async def claim(self, appeal_id: uuid.UUID, moderator_id: int) -> Appeal | None:
        result = await self.session.execute(
            update(Appeal)
            .where(
                Appeal.id == appeal_id,
                Appeal.status == AppealStatus.PENDING,
                (Appeal.assigned_to.is_(None) | (Appeal.assigned_to == moderator_id)),
            )
            .values(assigned_to=moderator_id)
            .returning(Appeal)
        )
        appeal = result.scalar_one_or_none()
        if appeal is not None:
            return appeal
        current = await self.get(appeal_id)
        if current is None or current.status != AppealStatus.PENDING:
            return None
        if current.assigned_to not in {None, moderator_id}:
            return None
        current.assigned_to = moderator_id
        await self.session.flush()
        return current

    async def release(self, appeal_id: uuid.UUID, moderator_id: int, *, override: bool = False) -> Appeal | None:
        conditions = [
            Appeal.id == appeal_id,
            Appeal.status == AppealStatus.PENDING,
            Appeal.assigned_to.is_not(None),
        ]
        if not override:
            conditions.append(Appeal.assigned_to == moderator_id)
        result = await self.session.execute(
            update(Appeal)
            .where(*conditions)
            .values(assigned_to=None)
            .returning(Appeal)
        )
        return result.scalar_one_or_none()

    async def resolve(self, appeal_id: uuid.UUID, status: AppealStatus, admin_id: int) -> Appeal | None:
        result = await self.session.execute(
            update(Appeal)
            .where(Appeal.id == appeal_id, Appeal.status == AppealStatus.PENDING)
            .values(
                status=status,
                admin_id=admin_id,
                reviewed_at=__import__("datetime").datetime.now(
                    __import__("datetime").timezone.utc
                ),
            )
            .returning(Appeal)
        )
        return result.scalar_one_or_none()
