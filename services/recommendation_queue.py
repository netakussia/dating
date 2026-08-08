from __future__ import annotations

import logging
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any, Protocol

from redis import Redis


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
    """Process-local queue implementation; retained for tests and local fallback."""

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


logger = logging.getLogger(__name__)


class RedisRecommendationQueue:
    def __init__(self, redis_client: Redis | Any) -> None:
        self._redis = redis_client

    def _key(self, user_id: int) -> str:
        return f"recommendation_queue:{user_id}"

    @staticmethod
    def _encode(entry: QueueEntry) -> str:
        return f"{entry.candidate_id}:{entry.score}"

    @staticmethod
    def _decode(raw: bytes | str | None) -> QueueEntry | None:
        if raw is None:
            return None
        text = raw.decode("utf-8") if isinstance(raw, bytes) else str(raw)
        candidate_id_str, score_str = text.split(":", 1)
        return QueueEntry(candidate_id=int(candidate_id_str), score=float(score_str))

    def replace(self, user_id: int, entries: list[QueueEntry]) -> None:
        key = self._key(user_id)
        self._redis.delete(key)
        if entries:
            self._redis.rpush(key, *[self._encode(entry) for entry in entries])

    def pop(self, user_id: int) -> QueueEntry | None:
        key = self._key(user_id)
        while True:
            raw = self._redis.lpop(key)
            if raw is None:
                return None
            try:
                return self._decode(raw)
            except (ValueError, UnicodeDecodeError) as error:
                logger.warning("Corrupted recommendation queue entry for user %s: %s", user_id, error)
                continue

    def move_to_end(self, user_id: int, candidate_id: int, score: float) -> None:
        key = self._key(user_id)
        entry = self._encode(QueueEntry(candidate_id, score))
        self._redis.eval(
            """
            local key = KEYS[1]
            local candidate_id = tonumber(ARGV[1])
            local entry = ARGV[2]
            local values = redis.call('LRANGE', key, 0, -1)
            local filtered = {}
            for i = 1, #values do
                local value = values[i]
                local id = tonumber(string.match(value, '^(.-):'))
                if id ~= candidate_id then
                    table.insert(filtered, value)
                end
            end
            redis.call('DEL', key)
            for i = 1, #filtered do
                redis.call('RPUSH', key, filtered[i])
            end
            redis.call('RPUSH', key, entry)
            return 1
            """,
            1,
            key,
            str(candidate_id),
            entry,
        )

    def remove(self, user_id: int, candidate_id: int) -> None:
        key = self._key(user_id)
        self._redis.eval(
            """
            local key = KEYS[1]
            local candidate_id = tonumber(ARGV[1])
            local values = redis.call('LRANGE', key, 0, -1)
            local filtered = {}
            for i = 1, #values do
                local value = values[i]
                local id = tonumber(string.match(value, '^(.-):'))
                if id ~= candidate_id then
                    table.insert(filtered, value)
                end
            end
            redis.call('DEL', key)
            for i = 1, #filtered do
                redis.call('RPUSH', key, filtered[i])
            end
            return 1
            """,
            1,
            key,
            str(candidate_id),
        )

    def clear(self, user_id: int) -> None:
        self._redis.delete(self._key(user_id))


_DEFAULT_QUEUE: RecommendationQueue | None = None


def get_default_queue() -> RecommendationQueue:
    global _DEFAULT_QUEUE
    if _DEFAULT_QUEUE is None:
        from redis import Redis as SyncRedis

        from config import get_settings

        _DEFAULT_QUEUE = RedisRecommendationQueue(SyncRedis.from_url(get_settings().redis_url))
    return _DEFAULT_QUEUE
