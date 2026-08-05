from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Block, Like, Profile, RecommendationView, User, UserStatus


class RecommendationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def profile(self, user_id: int) -> Profile | None:
        return await self.session.scalar(select(Profile).where(Profile.user_id == user_id))

    async def eligible_profiles(self, user_id: int) -> list[Profile]:
        liked_ids = select(Like.to_user_id).where(Like.from_user_id == user_id)
        blocked_ids = select(Block.blocked_id).where(Block.blocker_id == user_id)
        statement = select(Profile).join(User).where(
            Profile.user_id != user_id,
            Profile.is_visible.is_(True),
            Profile.moderation_locked.is_(False),
            User.status == UserStatus.ACTIVE,
            Profile.user_id.not_in(liked_ids),
            Profile.user_id.not_in(blocked_ids),
        )
        return list((await self.session.scalars(statement)).all())

    async def eligible_profile(self, user_id: int, candidate_id: int) -> Profile | None:
        liked_ids = select(Like.to_user_id).where(Like.from_user_id == user_id)
        blocked_ids = select(Block.blocked_id).where(Block.blocker_id == user_id)
        statement = select(Profile).join(User).where(
            Profile.user_id == candidate_id,
            Profile.user_id != user_id,
            Profile.is_visible.is_(True),
            Profile.moderation_locked.is_(False),
            User.status == UserStatus.ACTIVE,
            Profile.user_id.not_in(liked_ids),
            Profile.user_id.not_in(blocked_ids),
        )
        return await self.session.scalar(statement)

    async def active_profiles(self, user_id: int) -> list[Profile]:
        statement = select(Profile).join(User).where(
            Profile.user_id != user_id,
            Profile.is_visible.is_(True),
            Profile.moderation_locked.is_(False),
            User.status == UserStatus.ACTIVE,
        )
        return list((await self.session.scalars(statement)).all())

    async def record_view(self, viewer_id: int, candidate_id: int, score: float) -> RecommendationView:
        event = RecommendationView(viewer_id=viewer_id, candidate_id=candidate_id, score=score)
        self.session.add(event)
        await self.session.flush()
        return event
