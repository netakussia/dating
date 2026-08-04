from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session, self.model = session, model

    async def get(self, key: object) -> T | None:
        return await self.session.get(self.model, key)

    async def add(self, instance: T) -> T:
        self.session.add(instance)
        await self.session.flush()
        return instance
