import pytest

from services.recommendation import RecommendationService
from models.profile import Profile


class DummyProfile:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def test_compute_score_exact_matches():
    a = DummyProfile(age=20, district="Center", institution="Uni", interests=["music", "sport"])
    b = DummyProfile(age=21, district="Center", institution="Uni", interests=["music", "sport"])
    score = RecommendationService.compute_score(a, b)
    # district (35) + institution (25) + interests Jaccard (1 * 20) + age (~0.8 *20)
    assert pytest.approx(score, rel=1e-3) == 35 + 25 + 20 + (max(0.0, 1.0 - abs(20 - 21) / 5) * 20)


def test_compute_score_no_common_interests():
    a = DummyProfile(age=30, district="North", institution="College", interests=["cooking"])
    b = DummyProfile(age=27, district="South", institution="Other", interests=["gaming"]) 
    score = RecommendationService.compute_score(a, b)
    # district 0 + institution 0 + interests 0 + age
    expected_age = max(0.0, 1.0 - abs(30 - 27) / 5) * 20
    assert pytest.approx(score, rel=1e-3) == expected_age


def test_compute_score_empty_interests():
    a = DummyProfile(age=25, district="A", institution="I", interests=[])
    b = DummyProfile(age=25, district="A", institution="J", interests=[])
    score = RecommendationService.compute_score(a, b)
    # district match (35) + institution 0 + interests 0 + age 20
    assert pytest.approx(score, rel=1e-3) == 35 + 20
