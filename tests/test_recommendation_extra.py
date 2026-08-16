import asyncio
from types import SimpleNamespace

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from models import Gender
from services.recommendation import RecommendationService
from services.recommendation_queue import MemoryRecommendationQueue, QueueEntry


def profile(user_id: int, *, age: int = 24, district: str = "Center", interests: list[str] | None = None):
    return SimpleNamespace(
        user_id=user_id,
        gender=Gender.MALE if user_id % 2 else Gender.FEMALE,
        target_gender=Gender.FEMALE if user_id % 2 else Gender.MALE,
        age=age,
        district=district,
        institution="University",
        interests=interests or ["music"],
        bio="Люблю музыку, прогулки и кофе",
    )


class ErrorStrategy:
    def __init__(self, fail_for: set[int] | None = None):
        self.fail_for = set(fail_for or ())

    async def score(self, _viewer, candidate):
        if candidate.user_id in self.fail_for:
            raise RuntimeError("scoring failed")
        return float(candidate.user_id)


class NonFiniteStrategy:
    async def score(self, _viewer, candidate):
        return float("nan") if candidate.user_id == 2 else float(candidate.user_id)


class UnavailableQueue:
    async def pop(self, _user_id):
        raise RedisConnectionError("redis unavailable")


class FakeRepository:
    def __init__(self, mine, candidates):
        self.profiles = {mine.user_id: mine, **{c.user_id: c for c in candidates}}
        self.candidates = candidates
        self.views = []

    async def profile(self, user_id):
        return self.profiles.get(user_id)

    async def eligible_profiles(self, _user_id):
        return self.candidates

    async def eligible_profile(self, _user_id, candidate_id):
        return self.profiles.get(candidate_id)

    async def active_profiles(self, _user_id):
        return self.candidates

    async def record_view_once(self, viewer_id, candidate_id, score):
        if any(viewer == viewer_id and candidate == candidate_id for viewer, candidate, _ in self.views):
            return None
        self.views.append((viewer_id, candidate_id, score))
        return object()


@pytest.mark.asyncio
async def test_rebuild_skips_candidates_with_scoring_exceptions():
    mine = profile(1)
    c1 = profile(2)
    c2 = profile(4)
    repo = FakeRepository(mine, [c1, c2])
    strategy = ErrorStrategy(fail_for={2})
    svc = RecommendationService(None, queue=MemoryRecommendationQueue(), strategy=strategy)
    svc.repo = repo

    count = await svc.rebuild_queue(mine.user_id)
    # one candidate failed scoring and should be skipped
    assert count == 1


@pytest.mark.asyncio
async def test_rebuild_skips_non_finite_scores():
    mine = profile(1)
    c1, c2 = profile(2), profile(4)
    svc = RecommendationService(None, queue=MemoryRecommendationQueue(), strategy=NonFiniteStrategy())
    svc.repo = FakeRepository(mine, [c1, c2])

    assert await svc.rebuild_queue(mine.user_id) == 1
    recommendation = await svc.next_recommendation(mine.user_id)
    assert recommendation is not None
    assert recommendation.profile.user_id == c2.user_id


@pytest.mark.asyncio
async def test_redis_failure_uses_database_as_the_source_of_truth():
    mine = profile(1)
    candidate = profile(2)
    svc = RecommendationService(None, queue=UnavailableQueue())
    svc.repo = FakeRepository(mine, [candidate])

    recommendation = await svc.next_recommendation(mine.user_id)

    assert recommendation is not None
    assert recommendation.profile.user_id == candidate.user_id
    assert svc.repo.views == [(mine.user_id, candidate.user_id, recommendation.score)]


@pytest.mark.asyncio
async def test_concurrent_next_recommendation_no_duplicate_delivery():
    mine = profile(1)
    candidates = [profile(2), profile(3), profile(4)]
    repo = FakeRepository(mine, candidates)
    queue = MemoryRecommendationQueue()
    svc = RecommendationService(None, queue=queue)
    svc.repo = repo

    # rebuild queue
    await svc.rebuild_queue(mine.user_id)

    # run two concurrent next_recommendation calls
    r1, r2 = await asyncio.gather(svc.next_recommendation(mine.user_id), svc.next_recommendation(mine.user_id))

    ids = {r1.profile.user_id if r1 else None, r2.profile.user_id if r2 else None}
    # both results should not be the same candidate
    assert len(ids) == 2


@pytest.mark.asyncio
async def test_duplicate_queue_entries_are_claimed_only_once():
    mine = profile(1)
    candidate = profile(2)
    repo = FakeRepository(mine, [candidate])
    queue = MemoryRecommendationQueue()
    svc = RecommendationService(None, queue=queue)
    svc.repo = repo
    await queue.replace(1, [QueueEntry(candidate.user_id, 100.0), QueueEntry(candidate.user_id, 100.0)])

    first, second = await asyncio.gather(svc.next_recommendation(1), svc.next_recommendation(1))

    assert [item for item in (first, second) if item is not None]
    assert sum(item is not None for item in (first, second)) == 1
    assert repo.views == [(mine.user_id, candidate.user_id, 100.0)]
