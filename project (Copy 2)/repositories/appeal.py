import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Appeal, AppealStatus


class AppealRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: int, text: str) -> Appeal:
        appeal = Appeal(user_id=user_id, text=text)
        self.session.add(appeal)
        await self.session.flush()
        return appeal

    async def get(self, appeal_id: uuid.UUID) -> Appeal | None:
        return await self.session.get(Appeal, appeal_id)

    async def pending(self) -> list[Appeal]:
        statement = select(Appeal).where(Appeal.status == AppealStatus.PENDING).order_by(Appeal.created_at)
        return list((await self.session.scalars(statement)).all())

    async def resolve(self, appeal_id: uuid.UUID, status: AppealStatus, admin_id: int) -> Appeal | None:
        appeal = await self.get(appeal_id)
        if appeal and appeal.status == AppealStatus.PENDING:
            appeal.status = status
            appeal.admin_id = admin_id
            await self.session.flush()
        return appeal
