from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiogram.types import CallbackQuery, User

from middlewares.profile_required import ProfileRequiredMiddleware


@pytest.mark.asyncio
async def test_allows_when_current_user_has_profile(monkeypatch):
    middleware = ProfileRequiredMiddleware()
    handled = False

    async def handler(event, data):
        nonlocal handled
        handled = True
        return "handled"

    # force middleware to consider the event as one that requires profile
    monkeypatch.setattr(ProfileRequiredMiddleware, "_requires_profile", classmethod(lambda cls, event: True))

    async def fake_get_profile(self, user_id):
        return True

    monkeypatch.setattr("services.profile_service.ProfileService.get_profile", fake_get_profile)

    data = {"current_user": SimpleNamespace(id=42), "session": SimpleNamespace()}
    result = await middleware(handler, SimpleNamespace(), data)

    assert result == "handled"
    assert handled


@pytest.mark.asyncio
async def test_allows_when_event_from_user_has_profile(monkeypatch):
    middleware = ProfileRequiredMiddleware()
    handled = False

    async def handler(event, data):
        nonlocal handled
        handled = True
        return "handled"

    monkeypatch.setattr(ProfileRequiredMiddleware, "_requires_profile", classmethod(lambda cls, event: True))

    async def fake_get_profile(self, user_id):
        return True

    monkeypatch.setattr("services.profile_service.ProfileService.get_profile", fake_get_profile)

    data = {"event_from_user": SimpleNamespace(id=43), "session": SimpleNamespace()}
    result = await middleware(handler, SimpleNamespace(from_user=SimpleNamespace(id=43)), data)

    assert result == "handled"
    assert handled


@pytest.mark.asyncio
async def test_blocks_when_no_profile(monkeypatch):
    middleware = ProfileRequiredMiddleware()
    handled = False

    async def handler(event, data):
        nonlocal handled
        handled = True
        return "handled"

    monkeypatch.setattr(ProfileRequiredMiddleware, "_requires_profile", classmethod(lambda cls, event: True))

    async def fake_get_profile_none(self, user_id):
        return None

    monkeypatch.setattr("services.profile_service.ProfileService.get_profile", fake_get_profile_none)

    class FakeEvent:
        def __init__(self, from_user=None):
            self.from_user = from_user
            self.message = self

        async def answer(self, *args, **kwargs):
            return None

        async def message_answer(self, *args, **kwargs):
            return None

        async def answer_message(self, *args, **kwargs):
            return None

    data = {"current_user": SimpleNamespace(id=44), "session": SimpleNamespace()}
    result = await middleware(handler, FakeEvent(), data)

    assert result is None
    assert not handled


@pytest.mark.asyncio
async def test_requires_profile_for_verify_callback_and_inline_promo_text(monkeypatch):
    middleware = ProfileRequiredMiddleware()

    async def handler(event, data):
        return "handled"

    async def fake_get_profile(self, user_id):
        return True

    monkeypatch.setattr("services.profile_service.ProfileService.get_profile", fake_get_profile)

    event_with_inline_verify = SimpleNamespace(
        data="verify:start",
        from_user=SimpleNamespace(id=77),
        message=SimpleNamespace(answer=lambda *a, **k: None),
    )
    data = {"session": SimpleNamespace(), "current_user": SimpleNamespace(id=77)}
    assert await middleware(handler, event_with_inline_verify, data) == "handled"

    msg = SimpleNamespace(text="Верификация профиля", from_user=SimpleNamespace(id=78))
    data = {"session": SimpleNamespace(), "current_user": SimpleNamespace(id=78)}
    assert await middleware(handler, msg, data) == "handled"


def test_profile_create_is_not_profile_only_callback():
    callback = CallbackQuery(
        id="query",
        from_user=User(id=1, is_bot=False, first_name="Test"),
        chat_instance="chat",
        data="profile:create",
    )

    assert ProfileRequiredMiddleware._requires_profile(callback) is False


@pytest.mark.asyncio
async def test_banned_user_can_submit_appeal_state(monkeypatch):
    from aiogram.types import Chat, Message

    from middlewares.user import UserSyncMiddleware
    from states.appeal import AppealState

    user = User(id=7, is_bot=False, first_name="Blocked")
    db_user = SimpleNamespace(id=7, username=None, status="BANNED")
    session = SimpleNamespace()
    state = SimpleNamespace(get_state=AsyncMock(return_value=AppealState.enter_text.state))
    event = Message(
        message_id=1,
        date=datetime.now(UTC),
        chat=Chat(id=7, type="private"),
        from_user=user,
        text="valid appeal text",
    )
    handler = AsyncMock(return_value="handled")
    monkeypatch.setattr(
        "middlewares.user.UserRepository.get_or_create",
        AsyncMock(return_value=db_user),
    )

    result = await UserSyncMiddleware()(handler, event, {"event_from_user": user, "session": session, "state": state})

    assert result == "handled"
    handler.assert_awaited_once()
