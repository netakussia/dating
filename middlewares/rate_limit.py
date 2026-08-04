from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from redis.asyncio import Redis

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis) -> None: self.redis = redis
    async def __call__(self, handler: Callable[..., Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        user = data.get("event_from_user")
        if not user: return await handler(event, data)
        key = f"rate:{user.id}" 
        if await self.redis.set(key, "1", ex=1, nx=True): return await handler(event, data)
        return None
