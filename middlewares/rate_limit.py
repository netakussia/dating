import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from redis.asyncio import Redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self._fallback_last_seen: dict[int, float] = {}

    async def __call__(
        self, handler: Callable[..., Awaitable[Any]], event: TelegramObject, data: dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)
        key = f"rate:{user.id}"
        try:
            allowed = await self.redis.set(key, "1", ex=1, nx=True)
        except RedisError as error:
            # Keep a small local emergency limit while Redis is unavailable.
            # This preserves basic availability without leaving every process open to bursts.
            now = time.monotonic()
            last_seen = self._fallback_last_seen.get(user.id)
            if last_seen is not None and now - last_seen < 1:
                return None
            self._fallback_last_seen[user.id] = now
            logger.warning("Rate limiter unavailable; using local fallback: %s", error)
            return await handler(event, data)
        if allowed:
            return await handler(event, data)
        return None
