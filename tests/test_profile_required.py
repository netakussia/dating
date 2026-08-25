from types import SimpleNamespace

import pytest

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
