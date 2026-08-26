from __future__ import annotations

import asyncio
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

_local_locks: dict[int, asyncio.Lock] = {}


class PhotoUploadBusyError(RuntimeError):
    pass


@asynccontextmanager
async def photo_upload_lock(bot, user_id: int) -> AsyncIterator[None]:
    """Serialize photo updates across workers when the shared Redis client is available."""
    redis = getattr(bot, "notification_redis", None)
    if redis is None:
        lock = _local_locks.setdefault(user_id, asyncio.Lock())
        async with lock:
            yield
        return

    key = f"photo_upload:lock:{user_id}"
    token = uuid.uuid4().hex
    acquired = False
    try:
        for _ in range(40):
            if await redis.set(key, token, nx=True, ex=10):
                acquired = True
                break
            await asyncio.sleep(0.05)
        if not acquired:
            raise PhotoUploadBusyError("Photo upload is busy; please retry")
        yield
    finally:
        if acquired:
            try:
                await redis.eval(
                    "if redis.call('GET', KEYS[1]) == ARGV[1] then return redis.call('DEL', KEYS[1]) else return 0 end",
                    1,
                    key,
                    token,
                )
            except Exception:
                pass