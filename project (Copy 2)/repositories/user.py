from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, UserStatus
from repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None: super().__init__(session, User)
    async def get_or_create(self, user_id: int, username: str | None) -> User:
        user = await self.get(user_id)
        if user is None:
            user = await self.add(User(id=user_id, username=username))
        elif user.username != username:
            user.username = username
            await self.session.flush()
        return user
    async def by_username(self, username: str) -> User | None:
        return await self.session.scalar(select(User).where(User.username == username.lstrip("@")))
    async def active(self, user_id: int) -> bool:
        return await self.session.scalar(select(User.status == UserStatus.ACTIVE).where(User.id == user_id)) or False

    async def all_ids(self) -> list[int]:
        return list((await self.session.scalars(select(User.id).where(User.status != UserStatus.BANNED))).all())
