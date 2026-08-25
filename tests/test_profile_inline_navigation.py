from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from handlers.profile import promo_my_profile


@pytest.mark.asyncio
async def test_inline_my_profile_uses_callback_user_id(monkeypatch):
    show_profile = AsyncMock()
    monkeypatch.setattr("handlers.profile.show_profile", show_profile)
    message = SimpleNamespace()
    callback = SimpleNamespace(
        message=message,
        from_user=SimpleNamespace(id=42),
        answer=AsyncMock(),
    )
    session = SimpleNamespace()
    state = SimpleNamespace()

    await promo_my_profile(callback, session, state)

    callback.answer.assert_awaited_once()
    show_profile.assert_awaited_once_with(message, 42, session, state)
