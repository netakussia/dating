from __future__ import annotations

import logging
import math
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any, Protocol

import redis.asyncio as aioredis


@dataclass(frozen=True, slots=True)
class QueueEntry:
    candidate_id: int
    score: float


class RecommendationQueue(Protocol):
    async def replace(self, user_id: int, entries: list[QueueEntry]) -> None: ...
    async def pop(self, user_id: int) -> QueueEntry | None: ...
    async def move_to_end(self, user_id: int, candidate_id: int, score: float) -> None: ...
    async def remove(self, user_id: int, candidate_id: int) -> None: ...
    async def clear(self, user_id: int) -> None: ...


class MemoryRecommendationQueue:
    """Process-local queue implementation; retained for tests and local fallback."""

    def __init__(self) -> None:
        self._queues: dict[int, deque[QueueEntry]] = defaultdict(deque)

    async def replace(self, user_id: int, entries: list[QueueEntry]) -> None:
        self._queues[user_id] = deque(entries)

    async def pop(self, user_id: int) -> QueueEntry | None:
        queue = self._queues[user_id]
        return queue.popleft() if queue else None

    async def move_to_end(self, user_id: int, candidate_id: int, score: float) -> None:
        await self.remove(user_id, candidate_id)
        self._queues[user_id].append(QueueEntry(candidate_id, score))

    async def remove(self, user_id: int, candidate_id: int) -> None:
        self._queues[user_id] = deque(entry for entry in self._queues[user_id] if entry.candidate_id != candidate_id)

    async def clear(self, user_id: int) -> None:
        self._queues.pop(user_id, None)


logger = logging.getLogger(__name__)


class RedisRecommendationQueue:
    def __init__(self, redis_client: aioredis.Redis | Any) -> None:
        self._redis = redis_client

    def _key(self, user_id: int) -> str:
        return f"recommendation_queue:{user_id}"

    @staticmethod
    def _encode(entry: QueueEntry) -> str:
        if not math.isfinite(entry.score):
            raise ValueError("Recommendation score must be finite")
        return f"{entry.candidate_id}:{entry.score}"

    @staticmethod
    def _decode(raw: bytes | str | None) -> QueueEntry | None:
        if raw is None:
            return None
        text = raw.decode("utf-8") if isinstance(raw, bytes | bytearray) else str(raw)
        candidate_id_str, score_str = text.split(":", 1)
        entry = QueueEntry(candidate_id=int(candidate_id_str), score=float(score_str))
        if not math.isfinite(entry.score):
            raise ValueError("Recommendation score must be finite")
        return entry

    async def replace(self, user_id: int, entries: list[QueueEntry]) -> None:
        key = self._key(user_id)
        encoded: list[str] = []
        candidate_ids: set[int] = set()
        for entry in entries:
            if entry.candidate_id in candidate_ids:
                continue
            encoded.append(self._encode(entry))
            candidate_ids.add(entry.candidate_id)
        # DEL and RPUSH must be atomic so a concurrent pop cannot observe an
        # artificial empty queue and start an unnecessary rebuild.
        await self._redis.eval(
            """
            local key = KEYS[1]
            redis.call('DEL', key)
            for i = 1, #ARGV do
                redis.call('RPUSH', key, ARGV[i])
            end
            return #ARGV
            """,
            1,
            key,
            *encoded,
        )

    async def pop(self, user_id: int) -> QueueEntry | None:
        key = self._key(user_id)
        while True:
            raw = await self._redis.lpop(key)
            if raw is None:
                return None
            try:
                return self._decode(raw)
            except (ValueError, UnicodeDecodeError) as error:
                logger.warning("Corrupted recommendation queue entry for user %s: %s", user_id, error)
                continue

    async def move_to_end(self, user_id: int, candidate_id: int, score: float) -> None:
        key = self._key(user_id)
        entry = self._encode(QueueEntry(candidate_id, score))
        await self._redis.eval(
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

    async def remove(self, user_id: int, candidate_id: int) -> None:
        key = self._key(user_id)
        await self._redis.eval(
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

    async def clear(self, user_id: int) -> None:
        await self._redis.delete(self._key(user_id))


_DEFAULT_QUEUE: RecommendationQueue | None = None


def get_default_queue() -> RecommendationQueue:
    global _DEFAULT_QUEUE
    if _DEFAULT_QUEUE is None:
        from config import get_settings

        _DEFAULT_QUEUE = RedisRecommendationQueue(aioredis.Redis.from_url(get_settings().redis_url))
    return _DEFAULT_QUEUE
