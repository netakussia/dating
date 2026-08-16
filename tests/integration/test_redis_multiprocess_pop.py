import asyncio
import json
import os
import tempfile
from multiprocessing import Process
from pathlib import Path

import pytest
import redis.asyncio as aioredis

from services.recommendation_queue import QueueEntry, RedisRecommendationQueue

REDIS_URL = os.environ.get("REDIS_URL")
INTEGRATION = os.environ.get("INTEGRATION")


def _pop_once_process(redis_url: str, user_id: int, out_path: str):
    # Runs in a separate process: create an event loop and pop one entry
    import asyncio

    import redis.asyncio as aioredis

    from services.recommendation_queue import RedisRecommendationQueue

    async def _run():
        r = aioredis.Redis.from_url(redis_url)
        queue = RedisRecommendationQueue(r)
        try:
            entry = await queue.pop(user_id)
            result = (entry.candidate_id if entry else None)
        finally:
            await r.aclose()
        Path(out_path).write_text(json.dumps(result))

    asyncio.run(_run())


@pytest.mark.skipif(not INTEGRATION or not REDIS_URL, reason="Integration tests require INTEGRATION=1 and REDIS_URL")
def test_redis_pop_is_atomic_across_processes():
    redis_url = REDIS_URL
    user_id = 99999
    count = 10

    async def setup_list():
        r = aioredis.Redis.from_url(redis_url)
        key = f"recommendation_queue:{user_id}"
        await r.delete(key)
        # push 5 entries only
        entries = [f"{i}:{float(i)}" for i in range(2, 2 + (count // 2))]
        if entries:
            await r.rpush(key, *entries)
        await r.aclose()

    asyncio.run(setup_list())

    tmpdir = tempfile.TemporaryDirectory()
    procs = []
    out_files = []
    # spawn more processes than entries to ensure some get None
    for idx in range(count):
        out_path = Path(tmpdir.name) / f"result_{idx}.json"
        p = Process(target=_pop_once_process, args=(redis_url, user_id, str(out_path)))
        p.start()
        procs.append(p)
        out_files.append(out_path)

    for p in procs:
        p.join(timeout=30)
        if p.exitcode is None:
            p.terminate()

    # Collect results

    values = []
    for f in out_files:
        if f.exists():
            try:
                values.append(json.loads(f.read_text()))
            except Exception:
                values.append(None)
        else:
            values.append(None)

    # Unique non-None values should be equal to number of entries pushed
    non_none = [v for v in values if v is not None]
    assert len(set(non_none)) == (count // 2)
    tmpdir.cleanup()


@pytest.mark.skipif(not INTEGRATION or not REDIS_URL, reason="Integration tests require INTEGRATION=1 and REDIS_URL")
def test_redis_queue_skips_corrupted_entry(real_redis=True):
    # Push corrupted entry and a good one, ensure pop skips corrupted and returns valid
    redis_url = REDIS_URL
    user_id = 99998

    async def setup_list():
        r = aioredis.Redis.from_url(redis_url)
        key = f"recommendation_queue:{user_id}"
        await r.delete(key)
        await r.rpush(key, "bad-entry", "3:30")
        await r.aclose()

    asyncio.run(setup_list())

    async def run_pop():
        r = aioredis.Redis.from_url(redis_url)
        queue = RedisRecommendationQueue(r)
        first = await queue.pop(user_id)
        second = await queue.pop(user_id)
        await r.aclose()
        return first, second

    first, second = asyncio.run(run_pop())
    assert first == QueueEntry(3, 30.0)
    assert second is None
