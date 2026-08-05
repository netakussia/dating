from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from services.matching_stats import MatchingStats, MatchingStatsService
from services.recommendation import CandidateDiagnostic, RecommendationService
from services.recommendation_strategy import WeightedRecommendationStrategy


@dataclass(frozen=True, slots=True)
class MatchingDebugReport:
    stats: MatchingStats
    candidates: tuple[CandidateDiagnostic, ...]
    gender_compatible: int
    age_relevant: int
    same_district: int
    shared_interests: int


class MatchingDebugService:
    def __init__(self, session: AsyncSession, *, weights: dict[str, float]) -> None:
        self.recommendations = RecommendationService(session, weights=weights)
        self.stats = MatchingStatsService(session)

    async def report_for(self, user_id: int) -> MatchingDebugReport:
        candidates = tuple(await self.recommendations.diagnostics(user_id))
        included = [candidate for candidate in candidates if candidate.included]
        mine = await self.recommendations.repo.profile(user_id)
        profiles = {profile.user_id: profile for profile in await self.recommendations.repo.active_profiles(user_id)}
        components = [
            WeightedRecommendationStrategy.components(mine, profiles[item.candidate_id])
            for item in included
            if mine is not None and item.candidate_id in profiles
        ]
        return MatchingDebugReport(
            stats=await self.stats.snapshot(),
            candidates=candidates,
            gender_compatible=sum(
                "gender" not in item.reasons and "target_gender" not in item.reasons for item in candidates
            ),
            age_relevant=sum(item["age"] > 0 for item in components),
            same_district=sum(item["district"] > 0 for item in components),
            shared_interests=sum(item["interests"] > 0 for item in components),
        )
