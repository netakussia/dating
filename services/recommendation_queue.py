from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class QueueEntry:
    candidate_id: int
    score: float


class RecommendationQueue(Protocol):
    def replace(self, user_id: int, entries: list[QueueEntry]) -> None: ...
    def pop(self, user_id: int) -> QueueEntry | None: ...
    def move_to_end(self, user_id: int, candidate_id: int, score: float) -> None: ...
    def remove(self, user_id: int, candidate_id: int) -> None: ...
    def clear(self, user_id: int) -> None: ...


class MemoryRecommendationQueue:
    """Process-local queue implementation; it can be replaced by a Redis-backed adapter."""

    def __init__(self) -> None:
        self._queues: dict[int, deque[QueueEntry]] = defaultdict(deque)

    def replace(self, user_id: int, entries: list[QueueEntry]) -> None:
        self._queues[user_id] = deque(entries)

    def pop(self, user_id: int) -> QueueEntry | None:
        queue = self._queues[user_id]
        return queue.popleft() if queue else None

    def move_to_end(self, user_id: int, candidate_id: int, score: float) -> None:
        self.remove(user_id, candidate_id)
        self._queues[user_id].append(QueueEntry(candidate_id, score))

    def remove(self, user_id: int, candidate_id: int) -> None:
        self._queues[user_id] = deque(entry for entry in self._queues[user_id] if entry.candidate_id != candidate_id)

    def clear(self, user_id: int) -> None:
        self._queues.pop(user_id, None)
