from sqlalchemy.ext.asyncio import AsyncSession

from models import Like
from repositories.like import LikeRepository

class MatchService:
    def __init__(self, session: AsyncSession) -> None: self.repo = LikeRepository(session)
    async def like(self, source: int, target: int, comment: str | None = None) -> tuple[Like, bool]:
        like = await self.repo.add(source, target, comment)
        reciprocal = await self.repo.reciprocal(source, target)
        if reciprocal:
            like.is_mutual = reciprocal.is_mutual = True
            await self.repo.create_match(source, target)
            return like, True
        return like, False
