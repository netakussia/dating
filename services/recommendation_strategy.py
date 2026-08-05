from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Protocol

from models import Gender, Profile

DEFAULT_MATCHING_WEIGHTS: dict[str, float] = {
    "gender": 35.0,
    "target_gender": 25.0,
    "age": 10.0,
    "district": 10.0,
    "institution": 10.0,
    "interests": 7.0,
    "bio": 3.0,
}


class RecommendationStrategy(Protocol):
    """Asynchronous ranking contract for a compatible recommendation candidate."""

    async def score(self, viewer: Profile, candidate: Profile) -> float: ...


class WeightedRecommendationStrategy:
    """Deterministic strategy based on configurable compatibility weights."""

    def __init__(self, weights: Mapping[str, float] | None = None) -> None:
        self.weights = {**DEFAULT_MATCHING_WEIGHTS, **dict(weights or {})}
        unknown = self.weights.keys() - DEFAULT_MATCHING_WEIGHTS.keys()
        if unknown:
            raise ValueError(f"Неизвестные веса рекомендаций: {', '.join(sorted(unknown))}.")
        if any(
            isinstance(value, bool) or not isinstance(value, int | float) or value < 0
            for value in self.weights.values()
        ):
            raise ValueError("Веса рекомендаций должны быть неотрицательными числами.")
        if sum(self.weights.values()) <= 0:
            raise ValueError("Сумма весов рекомендаций должна быть больше нуля.")

    async def score(self, viewer: Profile, candidate: Profile) -> float:
        return self.score_sync(viewer, candidate)

    def score_sync(self, viewer: Profile, candidate: Profile) -> float:
        components = self.components(viewer, candidate)
        total_weight = sum(self.weights.values())
        return round(100 * sum(self.weights[name] * components[name] for name in self.weights) / total_weight, 1)

    @classmethod
    def components(cls, viewer: Profile, candidate: Profile) -> dict[str, float]:
        return {
            "gender": 1.0 if viewer.target_gender == Gender.ALL or candidate.gender == viewer.target_gender else 0.0,
            "target_gender": (
                1.0 if candidate.target_gender == Gender.ALL or candidate.target_gender == viewer.gender else 0.0
            ),
            "age": max(0.0, 1.0 - abs(viewer.age - candidate.age) / 20),
            "district": cls._text_match(viewer.district, candidate.district),
            "institution": cls._text_match(viewer.institution, candidate.institution),
            "interests": cls._jaccard(viewer.interests or [], candidate.interests or []),
            "bio": cls._jaccard(cls._tokens(viewer.bio), cls._tokens(candidate.bio)),
        }

    @staticmethod
    def _text_match(first: str, second: str) -> float:
        return 1.0 if first.strip().casefold() == second.strip().casefold() else 0.0

    @staticmethod
    def _tokens(value: str) -> list[str]:
        return re.findall(r"[\w-]+", value.casefold())

    @staticmethod
    def _jaccard(first: Iterable[str], second: Iterable[str]) -> float:
        first_values = {str(item).casefold() for item in first if str(item).strip()}
        second_values = {str(item).casefold() for item in second if str(item).strip()}
        union = first_values | second_values
        return len(first_values & second_values) / len(union) if union else 0.0
