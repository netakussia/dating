from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from models import Gender
from services.recommendation import RecommendationService
from services.recommendation_queue import MemoryRecommendationQueue, QueueEntry
from services.recommendation_strategy import WeightedRecommendationStrategy


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
        created_at=datetime(2026, 1, user_id % 28 + 1, tzinfo=UTC),
    )


class FakeRecommendationRepository:
    def __init__(self, mine, candidates):
        self.profiles = {mine.user_id: mine, **{item.user_id: item for item in candidates}}
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
 
    async def record_view(self, viewer_id, candidate_id, score):
        self.views.append((viewer_id, candidate_id, score))
 
 
class ViewedRecommendationRepository(FakeRecommendationRepository):
    async def eligible_profiles(self, _user_id):
        viewed = {candidate_id for viewer_id, candidate_id, _ in self.views if viewer_id == _user_id}
        return [candidate for candidate in self.candidates if candidate.user_id not in viewed]
 
    async def eligible_profile(self, _user_id, candidate_id):
        if any(viewer_id == _user_id and seen_candidate_id == candidate_id for viewer_id, seen_candidate_id, _ in self.views):
            return None
        return self.profiles.get(candidate_id)


class FixedRecommendationStrategy:
    async def score(self, _viewer, candidate):
        return float(candidate.user_id)


def service(mine, candidates):
    result = RecommendationService(None, queue=MemoryRecommendationQueue())
    result.repo = FakeRecommendationRepository(mine, candidates)
    return result


def test_compute_score_uses_configurable_default_weights():
    mine = profile(1, age=20)
    candidate = profile(2, age=21)

    assert RecommendationService.compute_score(mine, candidate) == 99.5


def test_normalize_text_matching_handles_aliases():
    from services.recommendation_strategy import WeightedRecommendationStrategy

    assert WeightedRecommendationStrategy._text_match("Bălți", "Бельцы") == 1.0
    assert WeightedRecommendationStrategy._text_match("CPB", "Colegiul Politehnic") == 1.0


def test_weighted_strategy_rejects_invalid_weight_configuration():
    with pytest.raises(ValueError, match="Неизвестные"):
        WeightedRecommendationStrategy({"unknown": 1})
    with pytest.raises(ValueError, match="Сумма"):
        WeightedRecommendationStrategy({name: 0 for name in WeightedRecommendationStrategy().weights})


@pytest.mark.asyncio
async def test_empty_database_or_one_user_has_no_recommendation():
    mine = profile(1)
    engine = service(mine, [])

    assert await engine.next_recommendation(mine.user_id) is None


@pytest.mark.asyncio
async def test_two_users_receive_ranked_recommendation_and_view_event():
    mine = profile(1)
    candidate = profile(2)
    engine = service(mine, [candidate])

    recommendation = await engine.next_recommendation(mine.user_id)

    assert recommendation is not None
    assert recommendation.profile is candidate
    assert recommendation.score == 100.0
    assert engine.repo.views == [(1, 2, 100.0)]


@pytest.mark.asyncio
async def test_engine_accepts_replacement_strategy_without_handler_changes():
    mine = profile(1)
    first, second = profile(2), profile(4)
    engine = RecommendationService(None, queue=MemoryRecommendationQueue(), strategy=FixedRecommendationStrategy())
    engine.repo = FakeRecommendationRepository(mine, [first, second])

    recommendation = await engine.next_recommendation(mine.user_id)

    assert recommendation is not None
    assert recommendation.profile is second
    assert recommendation.score == 4.0


@pytest.mark.asyncio
async def test_stale_queue_entry_is_skipped_without_recursion():
    mine, candidate = profile(1), profile(2)
    engine = service(mine, [candidate])
    engine.queue.replace(1, [QueueEntry(999, 99), QueueEntry(candidate.user_id, 90)])

    recommendation = await engine.next_recommendation(1)

    assert recommendation is not None
    assert recommendation.profile is candidate


@pytest.mark.asyncio
@pytest.mark.parametrize("candidate_count", [10, 100])
async def test_ten_and_hundred_candidates_are_sorted_without_duplicates(candidate_count):
    mine = profile(1)
    candidates = [
        profile(number, age=20 + number % 20, district="Center" if number % 3 else "North")
        for number in range(2, candidate_count + 2)
    ]
    for candidate in candidates:
        candidate.gender = Gender.FEMALE
        candidate.target_gender = Gender.MALE
    engine = service(mine, candidates)

    assert await engine.rebuild_queue(mine.user_id) == candidate_count
    delivered = []
    for _ in candidates:
        recommendation = await engine.next_recommendation(mine.user_id)
        assert recommendation is not None
        delivered.append(recommendation.profile.user_id)

    assert len(delivered) == candidate_count
    assert len(set(delivered)) == candidate_count
    assert delivered[0] == 4


@pytest.mark.asyncio
async def test_skip_moves_profile_to_end_of_current_queue():
    mine = profile(1)
    first, second, third = profile(2), profile(4, age=35), profile(6, age=38)
    engine = service(mine, [first, second, third])
 
    await engine.rebuild_queue(1)
    await engine.skip(1, first.user_id)
    delivered = [
        (await engine.next_recommendation(1)).profile.user_id,
        (await engine.next_recommendation(1)).profile.user_id,
        (await engine.next_recommendation(1)).profile.user_id,
    ]
 
    assert delivered[-1] == first.user_id
 
 
@pytest.mark.asyncio
async def test_viewed_profiles_are_excluded_from_recommendations():
    mine = profile(1)
    candidate = profile(2)
    engine = RecommendationService(None, queue=MemoryRecommendationQueue())
    engine.repo = ViewedRecommendationRepository(mine, [candidate])
    engine.repo.views.append((1, candidate.user_id, 80.0))
 
    await engine.rebuild_queue(mine.user_id)
 
    assert await engine.next_recommendation(mine.user_id) is None
 
 
def test_incompatible_gender_is_not_eligible_for_queue():
    mine, candidate = profile(1), profile(3)
    candidate.gender = Gender.MALE
    engine = service(mine, [candidate])

    assert not engine.is_compatible(mine, candidate)


@pytest.mark.asyncio
async def test_paused_or_blocked_profiles_are_not_delivered_when_repository_excludes_them():
    mine = profile(1)
    engine = service(mine, [])

    assert await engine.rebuild_queue(mine.user_id) == 0
    assert await engine.next_recommendation(mine.user_id) is None
