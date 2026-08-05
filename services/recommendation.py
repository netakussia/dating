from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from models import Gender, Profile
from repositories.recommendation import RecommendationRepository
from services.recommendation_queue import MemoryRecommendationQueue, QueueEntry, RecommendationQueue
from services.recommendation_strategy import (
    DEFAULT_MATCHING_WEIGHTS,
    RecommendationStrategy,
    WeightedRecommendationStrategy,
)

_DEFAULT_QUEUE = MemoryRecommendationQueue()


@dataclass(frozen=True, slots=True)
class Recommendation:
    profile: Profile
    score: float


@dataclass(frozen=True, slots=True)
class CandidateDiagnostic:
    candidate_id: int
    included: bool
    reasons: tuple[str, ...]
    score: float | None


class RecommendationService:
    def __init__(
        self,
        session: AsyncSession,
        *,
        weights: dict[str, float] | None = None,
        queue: RecommendationQueue | None = None,
        strategy: RecommendationStrategy | None = None,
    ) -> None:
        self.repo = RecommendationRepository(session)
        self.strategy = strategy or WeightedRecommendationStrategy(weights)
        self.queue = queue or _DEFAULT_QUEUE

    async def next_recommendation(self, user_id: int) -> Recommendation | None:
        mine = await self.repo.profile(user_id)
        if mine is None:
            return None
        entry = self.queue.pop(user_id)
        if entry is None:
            await self.rebuild_queue(user_id, mine)
            entry = self.queue.pop(user_id)
        while entry is not None:
            profile = await self.repo.eligible_profile(user_id, entry.candidate_id)
            if profile is None or not self.is_compatible(mine, profile):
                entry = self.queue.pop(user_id)
                continue
            await self.repo.record_view(user_id, profile.user_id, entry.score)
            return Recommendation(profile=profile, score=entry.score)
        return None

    async def next_profile(self, user_id: int) -> Profile | None:
        recommendation = await self.next_recommendation(user_id)
        return recommendation.profile if recommendation else None

    async def rebuild_queue(self, user_id: int, mine: Profile | None = None) -> int:
        mine = mine or await self.repo.profile(user_id)
        if mine is None:
            self.queue.clear(user_id)
            return 0
        candidates = await self.repo.eligible_profiles(user_id)
        entries = []
        for candidate in candidates:
            if self.is_compatible(mine, candidate):
                entries.append(QueueEntry(candidate.user_id, await self.strategy.score(mine, candidate)))
        entries.sort(key=lambda entry: (-entry.score, entry.candidate_id))
        self.queue.replace(user_id, entries)
        return len(entries)

    async def skip(self, user_id: int, candidate_id: int) -> None:
        mine = await self.repo.profile(user_id)
        candidate = await self.repo.profile(candidate_id)
        if mine is not None and candidate is not None and self.is_compatible(mine, candidate):
            self.queue.move_to_end(user_id, candidate_id, await self.strategy.score(mine, candidate))

    def remove_candidate(self, user_id: int, candidate_id: int) -> None:
        self.queue.remove(user_id, candidate_id)

    @staticmethod
    def is_compatible(mine: Profile, candidate: Profile) -> bool:
        gender_ok = mine.target_gender == Gender.ALL or candidate.gender == mine.target_gender
        target_ok = candidate.target_gender == Gender.ALL or candidate.target_gender == mine.gender
        return gender_ok and target_ok

    @staticmethod
    def compute_score(mine: Profile, candidate: Profile) -> float:
        """Compatibility score using the default weights; retained as a stable public helper."""
        return WeightedRecommendationStrategy(DEFAULT_MATCHING_WEIGHTS).score_sync(mine, candidate)

    async def diagnostics(self, user_id: int) -> list[CandidateDiagnostic]:
        mine = await self.repo.profile(user_id)
        if mine is None:
            return []
        active = await self.repo.active_profiles(user_id)
        eligible_ids = {profile.user_id for profile in await self.repo.eligible_profiles(user_id)}
        diagnostics: list[CandidateDiagnostic] = []
        for candidate in active:
            reasons: list[str] = []
            if candidate.user_id not in eligible_ids:
                reasons.append("already_liked_or_blocked")
            if mine.target_gender != Gender.ALL and candidate.gender != mine.target_gender:
                reasons.append("gender")
            if candidate.target_gender != Gender.ALL and candidate.target_gender != mine.gender:
                reasons.append("target_gender")
            included = not reasons
            diagnostics.append(
                CandidateDiagnostic(
                    candidate.user_id,
                    included,
                    tuple(reasons),
                    await self.strategy.score(mine, candidate) if included else None,
                )
            )
        return diagnostics
