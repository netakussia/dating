import pytest

from services.recommendation_queue import QueueEntry, RedisRecommendationQueue


class FakeRedis:
    def __init__(self):
        self.store = {}

    async def delete(self, key):
        self.store.pop(key, None)

    async def rpush(self, key, *values):
        self.store.setdefault(key, []).extend(values)

    async def lpop(self, key):
        values = self.store.get(key)
        if not values:
            return None
        return values.pop(0)

    async def eval(self, script, numkeys, *args):
        key = args[0]
        if "for i = 1, #ARGV do" in script:
            self.store[key] = list(args[1:])
            return len(args) - 1
        candidate_id = int(args[1])
        values = list(self.store.get(key, []))
        if "entry" in script:
            filtered = [value for value in values if self._candidate_id(value) != candidate_id]
            self.store[key] = filtered + [args[2]]
        else:
            self.store[key] = [value for value in values if self._candidate_id(value) != candidate_id]
        return 1

    @staticmethod
    def _candidate_id(raw):
        return int(str(raw).split(":", 1)[0])


@pytest.mark.asyncio
async def test_redis_queue_replace_and_pop_are_ordered_and_persistent():
    redis = FakeRedis()
    queue = RedisRecommendationQueue(redis)

    await queue.replace(1, [QueueEntry(2, 10.0), QueueEntry(3, 20.0)])

    assert await queue.pop(1) == QueueEntry(2, 10.0)
    assert await queue.pop(1) == QueueEntry(3, 20.0)
    assert await queue.pop(1) is None


@pytest.mark.asyncio
async def test_redis_queue_replace_deduplicates_candidates():
    redis = FakeRedis()
    queue = RedisRecommendationQueue(redis)

    await queue.replace(1, [QueueEntry(2, 10.0), QueueEntry(2, 20.0), QueueEntry(3, 30.0)])

    assert await queue.pop(1) == QueueEntry(2, 10.0)
    assert await queue.pop(1) == QueueEntry(3, 30.0)
    assert await queue.pop(1) is None


@pytest.mark.asyncio
async def test_redis_queue_move_to_end_and_remove_keep_the_expected_entries():
    redis = FakeRedis()
    queue = RedisRecommendationQueue(redis)

    await queue.replace(1, [QueueEntry(2, 10.0), QueueEntry(3, 20.0), QueueEntry(4, 30.0)])
    await queue.move_to_end(1, 3, 25.0)
    await queue.remove(1, 2)

    assert await queue.pop(1) == QueueEntry(4, 30.0)
    assert await queue.pop(1) == QueueEntry(3, 25.0)
    assert await queue.pop(1) is None


@pytest.mark.asyncio
async def test_redis_queue_skips_corrupted_entries_and_returns_next_valid_entry():
    redis = FakeRedis()
    queue = RedisRecommendationQueue(redis)

    redis.store["recommendation_queue:1"] = ["bad-entry", "3:30"]

    assert await queue.pop(1) == QueueEntry(3, 30.0)
    assert await queue.pop(1) is None
