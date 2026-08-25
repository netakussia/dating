from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, UserStatus
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None: super().__init__(session, User)
    async def get_or_create(self, user_id: int, username: str | None) -> User:
        normalized_username = username.casefold() if username else None
        user = await self.get(user_id)
        if user is None:
            user = await self.add(User(id=user_id, username=normalized_username))
        elif user.username != normalized_username:
            user.username = normalized_username
            await self.session.flush()
        return user
    async def by_username(self, username: str) -> User | None:
        normalized = username.lstrip("@").casefold()
        return await self.session.scalar(select(User).where(func.lower(User.username) == normalized))
    async def active(self, user_id: int) -> bool:
        status = await self.session.scalar(select(User.status).where(User.id == user_id))
        return (status == UserStatus.ACTIVE) if status is not None else False

    async def all_ids(self) -> list[int]:
        return list((await self.session.scalars(select(User.id).where(User.status == UserStatus.ACTIVE))).all())
