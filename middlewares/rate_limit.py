import logging
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
            # Rate limiting is anti-abuse state, not a reason to make the bot
            # unavailable when Redis is temporarily down.
            logger.warning("Rate limiter unavailable; allowing update: %s", error)
            return await handler(event, data)
        if allowed:
            return await handler(event, data)
        return None
