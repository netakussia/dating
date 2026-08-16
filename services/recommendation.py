from __future__ import annotations

import logging
import math
from dataclasses import dataclass

from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Gender, Profile
from repositories.recommendation import RecommendationRepository
from services.recommendation_queue import QueueEntry, RecommendationQueue, get_default_queue
from services.recommendation_strategy import (
    DEFAULT_MATCHING_WEIGHTS,
    RecommendationStrategy,
    WeightedRecommendationStrategy,
)


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
        self.queue = queue or get_default_queue()

    async def next_recommendation(self, user_id: int) -> Recommendation | None:
        mine = await self.repo.profile(user_id)
        if mine is None:
            return None
        try:
            return await self._next_from_queue(user_id, mine)
        except RedisError as error:
            logging.getLogger(__name__).warning(
                "Recommendation queue unavailable for user %s; using database fallback: %s", user_id, error
            )
            return await self._next_from_database(user_id, mine)

    async def _next_from_queue(self, user_id: int, mine: Profile) -> Recommendation | None:
        entry = await self.queue.pop(user_id)
        if entry is None:
            await self.rebuild_queue(user_id, mine)
            entry = await self.queue.pop(user_id)
        while entry is not None:
            profile = await self.repo.eligible_profile(user_id, entry.candidate_id)
            if profile is None or not self.is_compatible(mine, profile):
                entry = await self.queue.pop(user_id)
                continue
            if await self.repo.record_view_once(user_id, profile.user_id, entry.score) is not None:
                return Recommendation(profile=profile, score=entry.score)
            entry = await self.queue.pop(user_id)
        return None

    async def _next_from_database(self, user_id: int, mine: Profile) -> Recommendation | None:
        """Serve one card when disposable Redis state is temporarily unavailable."""
        candidates = await self.repo.eligible_profiles(user_id)
        ranked: list[QueueEntry] = []
        for candidate in candidates:
            if not self.is_compatible(mine, candidate):
                continue
            try:
                score = float(await self.strategy.score(mine, candidate))
            except Exception as error:
                logging.getLogger(__name__).warning(
                    "Error scoring database-fallback candidate %s for user %s: %s", candidate.user_id, user_id, error
                )
                continue
            if math.isfinite(score):
                ranked.append(QueueEntry(candidate.user_id, score))
        for entry in sorted(ranked, key=lambda item: (-item.score, item.candidate_id)):
            profile = await self.repo.eligible_profile(user_id, entry.candidate_id)
            if profile is None:
                continue
            if await self.repo.record_view_once(user_id, profile.user_id, entry.score) is not None:
                return Recommendation(profile=profile, score=entry.score)
        return None

    async def next_profile(self, user_id: int) -> Profile | None:
        recommendation = await self.next_recommendation(user_id)
        return recommendation.profile if recommendation else None

    async def rebuild_queue(self, user_id: int, mine: Profile | None = None) -> int:
        import asyncio
        import logging

        logger = logging.getLogger(__name__)

        mine = mine or await self.repo.profile(user_id)
        if mine is None:
            await self.queue.clear(user_id)
            return 0
        candidates = await self.repo.eligible_profiles(user_id)
        # Filter compatible candidates first to avoid unnecessary scoring
        candidates_to_score = [candidate for candidate in candidates if self.is_compatible(mine, candidate)]
        entries: list[QueueEntry] = []
        if candidates_to_score:
            # Compute scores concurrently to improve rebuild latency for large pools.
            coros = [self.strategy.score(mine, candidate) for candidate in candidates_to_score]
            results = await asyncio.gather(*coros, return_exceptions=True)
            for candidate, result in zip(candidates_to_score, results):
                if isinstance(result, Exception):
                    logger.exception("Error scoring candidate %s for user %s: %s", candidate.user_id, user_id, result)
                    # Skip candidates that failed scoring
                    continue
                try:
                    score = float(result)
                except (TypeError, ValueError):
                    logger.warning("Invalid score returned for candidate %s: %r", candidate.user_id, result)
                    continue
                if not math.isfinite(score):
                    logger.warning("Non-finite score returned for candidate %s: %r", candidate.user_id, result)
                    continue
                entries.append(QueueEntry(candidate.user_id, score))
        entries.sort(key=lambda entry: (-entry.score, entry.candidate_id))
        await self.queue.replace(user_id, entries)
        return len(entries)

    async def skip(self, user_id: int, candidate_id: int) -> None:
        mine = await self.repo.profile(user_id)
        candidate = await self.repo.profile(candidate_id)
        if mine is not None and candidate is not None and self.is_compatible(mine, candidate):
            try:
                await self.queue.move_to_end(user_id, candidate_id, await self.strategy.score(mine, candidate))
            except RedisError as error:
                logging.getLogger(__name__).warning(
                    "Could not update recommendation queue for skipped candidate %s: %s", candidate_id, error
                )

    async def remove_candidate(self, user_id: int, candidate_id: int) -> None:
        try:
            await self.queue.remove(user_id, candidate_id)
        except RedisError as error:
            logging.getLogger(__name__).warning(
                "Could not remove candidate %s from recommendation queue: %s", candidate_id, error
            )

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
                reasons.append("already_viewed_or_excluded")
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
