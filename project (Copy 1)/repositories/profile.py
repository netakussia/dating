from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Profile
from repositories.base import BaseRepository

class ProfileRepository(BaseRepository[Profile]):
    def __init__(self, session: AsyncSession) -> None: super().__init__(session, Profile)
    async def by_user_id(self, user_id: int) -> Profile | None:
        return await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
    async def save(self, profile: Profile) -> Profile:
        self.session.add(profile); await self.session.flush(); return profile
