from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Like


class LikeRepository:
    def __init__(self, session: AsyncSession) -> None: self.session = session
    async def exists(self, source: int, target: int) -> bool:
        statement = select(Like.id).where(Like.from_user_id == source, Like.to_user_id == target)
        return bool(await self.session.scalar(statement))
    async def add(self, source: int, target: int, comment: str | None = None) -> tuple[Like, bool]:
        existing = await self.session.scalar(select(Like).where(Like.from_user_id == source, Like.to_user_id == target))
        if existing:
            return existing, False
        like = Like(from_user_id=source, to_user_id=target, comment=comment)
        try:
            async with self.session.begin_nested():
                self.session.add(like)
                await self.session.flush()
        except IntegrityError:
            existing = await self.session.scalar(
                select(Like).where(Like.from_user_id == source, Like.to_user_id == target)
            )
            if existing is not None:
                return existing, False
            raise
        return like, True
    async def reciprocal(self, source: int, target: int) -> Like | None:
        return await self.session.scalar(select(Like).where(Like.from_user_id == target, Like.to_user_id == source))
