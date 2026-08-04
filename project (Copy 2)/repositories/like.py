from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Like, Match

class LikeRepository:
    def __init__(self, session: AsyncSession) -> None: self.session = session
    async def exists(self, source: int, target: int) -> bool:
        return bool(await self.session.scalar(select(Like.id).where(Like.from_user_id == source, Like.to_user_id == target)))
    async def add(self, source: int, target: int, comment: str | None = None) -> Like:
        existing = await self.session.scalar(select(Like).where(Like.from_user_id == source, Like.to_user_id == target))
        if existing:
            return existing
        like = Like(from_user_id=source, to_user_id=target, comment=comment)
        self.session.add(like); await self.session.flush(); return like
    async def reciprocal(self, source: int, target: int) -> Like | None:
        return await self.session.scalar(select(Like).where(Like.from_user_id == target, Like.to_user_id == source))
    async def create_match(self, a: int, b: int) -> Match:
        first, second = sorted((a, b))
        existing = await self.session.scalar(select(Match).where(Match.user1_id == first, Match.user2_id == second))
        if existing:
            return existing
        match = Match(user1_id=first, user2_id=second)
        self.session.add(match); await self.session.flush(); return match
