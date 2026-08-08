from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from models import Like, Match
from repositories.like import LikeRepository
from repositories.match import MatchRepository
from services.eligibility import EligibilityError, EligibilityService


@dataclass(frozen=True, slots=True)
class MatchResult:
    match: Match | None
    created: bool


class MatchService:
    """Owns mutual-like detection and idempotent Match persistence."""

    def __init__(self, session: AsyncSession) -> None:
        self.likes = LikeRepository(session)
        self.matches = MatchRepository(session)

    async def create_if_mutual(self, source_id: int, target_id: int, like: Like) -> MatchResult:
        try:
            await EligibilityService(self.likes.session).ensure_action_allowed(
                source_id,
                target_id,
                action="создать мэтч",
            )
            await EligibilityService(self.likes.session).ensure_action_allowed(
                target_id,
                source_id,
                action="создать мэтч",
            )
        except EligibilityError:
            return MatchResult(match=None, created=False)

        reciprocal = await self.likes.reciprocal(source_id, target_id)
        if reciprocal is None:
            return MatchResult(match=None, created=False)
        like.is_mutual = True
        reciprocal.is_mutual = True
        match, created = await self.matches.create_once(source_id, target_id)
        return MatchResult(match=match, created=created)

    async def matches_for(self, user_id: int, limit: int = 50) -> list[Match]:
        return await self.matches.by_user_id(user_id, limit)
