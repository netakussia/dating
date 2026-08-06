from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Block, Dislike, Like, ModerationStatus, Profile, RecommendationView, User, UserStatus


class RecommendationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def profile(self, user_id: int) -> Profile | None:
        return await self.session.scalar(select(Profile).where(Profile.user_id == user_id))

    async def eligible_profiles(self, user_id: int) -> list[Profile]:
        liked_ids = select(Like.to_user_id).where(Like.from_user_id == user_id)
        disliked_ids = select(Dislike.to_user_id).where(Dislike.from_user_id == user_id)
        blocked_by_me = select(Block.blocked_id).where(Block.blocker_id == user_id)
        blocked_me = select(Block.blocker_id).where(Block.blocked_id == user_id)
        viewed_ids = select(RecommendationView.candidate_id).where(RecommendationView.viewer_id == user_id)
        statement = (
            select(Profile)
            .join(User)
            .where(
                Profile.user_id != user_id,
                Profile.is_visible.is_(True),
                Profile.moderation_locked.is_(False),
                Profile.moderation_status == ModerationStatus.CLEAR,
                User.status == UserStatus.ACTIVE,
                Profile.user_id.not_in(liked_ids),
                Profile.user_id.not_in(disliked_ids),
                Profile.user_id.not_in(blocked_by_me),
                Profile.user_id.not_in(blocked_me),
                Profile.user_id.not_in(viewed_ids),
            )
        )
        return list((await self.session.scalars(statement)).all())

    async def eligible_profile(self, user_id: int, candidate_id: int) -> Profile | None:
        liked_ids = select(Like.to_user_id).where(Like.from_user_id == user_id)
        disliked_ids = select(Dislike.to_user_id).where(Dislike.from_user_id == user_id)
        blocked_by_me = select(Block.blocked_id).where(Block.blocker_id == user_id)
        blocked_me = select(Block.blocker_id).where(Block.blocked_id == user_id)
        viewed_ids = select(RecommendationView.candidate_id).where(RecommendationView.viewer_id == user_id)
        statement = (
            select(Profile)
            .join(User)
            .where(
                Profile.user_id == candidate_id,
                Profile.user_id != user_id,
                Profile.is_visible.is_(True),
                Profile.moderation_locked.is_(False),
                Profile.moderation_status == ModerationStatus.CLEAR,
                User.status == UserStatus.ACTIVE,
                Profile.user_id.not_in(liked_ids),
                Profile.user_id.not_in(disliked_ids),
                Profile.user_id.not_in(blocked_by_me),
                Profile.user_id.not_in(blocked_me),
                Profile.user_id.not_in(viewed_ids),
            )
        )
        return await self.session.scalar(statement)

    async def active_profiles(self, user_id: int) -> list[Profile]:
        disliked_ids = select(Dislike.to_user_id).where(Dislike.from_user_id == user_id)
        blocked_by_me = select(Block.blocked_id).where(Block.blocker_id == user_id)
        blocked_me = select(Block.blocker_id).where(Block.blocked_id == user_id)
        statement = (
            select(Profile)
            .join(User)
            .where(
                Profile.user_id != user_id,
                Profile.is_visible.is_(True),
                Profile.moderation_locked.is_(False),
                Profile.moderation_status == ModerationStatus.CLEAR,
                User.status == UserStatus.ACTIVE,
                Profile.user_id.not_in(disliked_ids),
                Profile.user_id.not_in(blocked_by_me),
                Profile.user_id.not_in(blocked_me),
            )
        )
        return list((await self.session.scalars(statement)).all())

    async def record_view(self, viewer_id: int, candidate_id: int, score: float) -> RecommendationView:
        event = RecommendationView(viewer_id=viewer_id, candidate_id=candidate_id, score=score)
        self.session.add(event)
        await self.session.flush()
        return event
