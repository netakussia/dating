from types import SimpleNamespace

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from middlewares.rate_limit import RateLimitMiddleware


class UnavailableRedis:
    async def set(self, *_args, **_kwargs):
        raise RedisConnectionError("redis unavailable")


@pytest.mark.asyncio
async def test_rate_limit_allows_update_when_redis_is_unavailable():
    middleware = RateLimitMiddleware(UnavailableRedis())
    handled = False

    async def handler(_event, _data):
        nonlocal handled
        handled = True
        return "handled"

    result = await middleware(handler, object(), {"event_from_user": SimpleNamespace(id=42)})

    assert result == "handled"
    assert handled

    second_result = await middleware(handler, object(), {"event_from_user": SimpleNamespace(id=42)})

    assert second_result is None
    assert handled is True
