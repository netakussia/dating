import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Confession, ConfessionStatus

class ConfessionRepository:
    def __init__(self, session: AsyncSession) -> None: self.session = session
    async def add(self, confession: Confession) -> Confession:
        self.session.add(confession); await self.session.flush(); return confession
    async def get_pending(self, confession_id: uuid.UUID) -> Confession | None:
        return await self.session.scalar(select(Confession).where(Confession.id == confession_id, Confession.status == ConfessionStatus.PENDING))
