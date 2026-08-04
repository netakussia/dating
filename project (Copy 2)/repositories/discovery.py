from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Block, Dislike, Like, Match, Profile, User


class DiscoveryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def skip(self, source_id: int, target_id: int) -> None:
        existing = await self.session.scalar(
            select(Dislike).where(Dislike.from_user_id == source_id, Dislike.to_user_id == target_id)
        )
        if existing is None:
            self.session.add(Dislike(from_user_id=source_id, to_user_id=target_id))
            await self.session.flush()

    async def block(self, blocker_id: int, blocked_id: int) -> None:
        existing = await self.session.scalar(
            select(Block).where(Block.blocker_id == blocker_id, Block.blocked_id == blocked_id)
        )
        if existing is None:
            self.session.add(Block(blocker_id=blocker_id, blocked_id=blocked_id))
            await self.session.flush()

    async def received_likes(self, user_id: int) -> list[Like]:
        return list((await self.session.scalars(
            select(Like).where(Like.to_user_id == user_id).order_by(Like.created_at.desc())
        )).all())

    async def matches(self, user_id: int) -> list[Match]:
        return list((await self.session.scalars(
            select(Match).where((Match.user1_id == user_id) | (Match.user2_id == user_id)).order_by(Match.created_at.desc())
        )).all())

    async def profile_and_user(self, user_id: int) -> tuple[Profile | None, User | None]:
        return (
            await self.session.scalar(select(Profile).where(Profile.user_id == user_id)),
            await self.session.get(User, user_id),
        )
