import time
import tracemalloc
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from models import Gender
from services.recommendation import RecommendationService
from services.recommendation_queue import MemoryRecommendationQueue


class FixedStrategy:
    async def score(self, _viewer, candidate):
        return float(candidate.user_id)


class PerformanceRepository:
    def __init__(self, mine, candidates):
        self.mine = mine
        self.candidates = candidates
        self.query_count = 0

    async def profile(self, user_id):
        if user_id == self.mine.user_id:
            return self.mine
        return None

    async def eligible_profiles(self, _user_id):
        self.query_count += 1
        return self.candidates

    async def eligible_profile(self, _user_id, candidate_id):
        self.query_count += 1
        return next((candidate for candidate in self.candidates if candidate.user_id == candidate_id), None)

    async def active_profiles(self, _user_id):
        return self.candidates

    async def record_view(self, viewer_id, candidate_id, score):
        return None


def profile(user_id: int):
    return SimpleNamespace(
        user_id=user_id,
        gender=Gender.MALE if user_id % 2 else Gender.FEMALE,
        target_gender=Gender.FEMALE if user_id % 2 else Gender.MALE,
        age=24,
        district="Center",
        institution="University",
        interests=["music"],
        bio="Люблю музыку",
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("candidate_count", [50, 200, 500, 1000, 2000, 5000])
async def test_recommendation_service_handles_large_candidate_sets(candidate_count):
    mine = profile(1)
    candidates = [profile(candidate_id) for candidate_id in range(2, candidate_count + 2)]
    for candidate in candidates:
        candidate.gender = Gender.FEMALE
        candidate.target_gender = Gender.MALE
    service = RecommendationService(None, queue=MemoryRecommendationQueue(), strategy=FixedStrategy())
    service.repo = PerformanceRepository(mine, candidates)

    tracemalloc.start()
    start_cpu = time.process_time()
    start_wall = time.perf_counter()
    queue_size = await service.rebuild_queue(mine.user_id)
    build_cpu = time.process_time() - start_cpu
    build_wall = time.perf_counter() - start_wall
    first_start_cpu = time.process_time()
    first_start_wall = time.perf_counter()
    first = await service.next_recommendation(mine.user_id)
    first_cpu = time.process_time() - first_start_cpu
    first_wall = time.perf_counter() - first_start_wall
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert queue_size == candidate_count
    assert first is not None
    assert first.profile.user_id == candidate_count + 1
    assert service.repo.query_count <= candidate_count + 2

    print(
        f"count={candidate_count} queue_build_ms={build_wall * 1000:.2f} "
        f"first_profile_ms={first_wall * 1000:.2f} queries={service.repo.query_count} "
        f"cpu_ms={build_cpu * 1000:.2f}/{first_cpu * 1000:.2f} mem_kib={peak / 1024:.2f}"
    )
