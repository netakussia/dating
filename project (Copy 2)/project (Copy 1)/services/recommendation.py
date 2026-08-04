from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Block, Dislike, Gender, Like, Profile, User, UserStatus

class RecommendationService:
    def __init__(self, session: AsyncSession) -> None: self.session = session
    async def next_profile(self, user_id: int) -> Profile | None:
        mine = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        if mine is None: return None
        liked_ids = select(Like.to_user_id).where(Like.from_user_id == user_id)
        skipped_ids = select(Dislike.to_user_id).where(Dislike.from_user_id == user_id)
        # Do not show either side of a block relationship.
        blocked_ids = select(Block.blocked_id).where(Block.blocker_id == user_id)
        blocked_by_ids = select(Block.blocker_id).where(Block.blocked_id == user_id)
        gender_filter = True if mine.target_gender == Gender.ALL else Profile.gender == mine.target_gender
        target_filter = (Profile.target_gender == Gender.ALL) | (Profile.target_gender == mine.gender)
        candidates = list((await self.session.scalars(select(Profile).join(User).where(
            Profile.user_id != user_id, Profile.is_visible.is_(True), User.status == UserStatus.ACTIVE,
            Profile.user_id.not_in(liked_ids),
            Profile.user_id.not_in(skipped_ids),
            Profile.user_id.not_in(blocked_ids),
            Profile.user_id.not_in(blocked_by_ids),
            gender_filter, target_filter,
        ))).all())
        def score(profile: Profile) -> tuple[float, object]:
            """Exact product formula: district 35 + institution 25 + Jaccard 20 + age 20."""
            mine_interests = {item.casefold() for item in mine.interests}
            profile_interests = {item.casefold() for item in profile.interests}
            union = mine_interests | profile_interests
            interest_score = len(mine_interests & profile_interests) / len(union) if union else 0.0
            age_score = max(0.0, 1.0 - abs(mine.age - profile.age) / 5)
            total = (
                35.0 * (profile.district.casefold() == mine.district.casefold())
                + 25.0 * (profile.institution.casefold() == mine.institution.casefold())
                + 20.0 * interest_score
                + 20.0 * age_score
            )
            # Creation time makes equal scores deterministic: newer profiles are first.
            return total, profile.created_at

        return max(candidates, key=score, default=None)
