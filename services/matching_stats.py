from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.matching_stats import MatchingStatsRepository


@dataclass(frozen=True, slots=True)
class MatchingStats:
    users: int
    active_users: int
    views: int
    likes: int
    matches: int
    reports: int
    ctr: float
    average_compatibility: float


class MatchingStatsService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = MatchingStatsRepository(session)

    async def snapshot(self) -> MatchingStats:
        return MatchingStats(**await self.repo.snapshot())
