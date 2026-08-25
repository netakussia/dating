from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from handlers.verification import verification_start
from services.profile_service import ProfileService
from states.verification import VerificationState


@pytest.mark.asyncio
async def test_verification_start_shows_status_if_already_verified(monkeypatch):
    # Prepare a fake profile marked as VERIFIED
    fake_profile = SimpleNamespace(verification_status=SimpleNamespace(value="VERIFIED"))

    async def fake_get_profile(self, user_id: int):
        return fake_profile

    monkeypatch.setattr(ProfileService, "get_profile", fake_get_profile)

    message = SimpleNamespace(from_user=SimpleNamespace(id=7), answer=AsyncMock())
    state = SimpleNamespace(set_state=AsyncMock())

    # Call handler
    await verification_start(message, state, session=None)

    # Should not set FSM state and should answer with verified status
    assert not state.set_state.called
    message.answer.assert_called_once()
    called_text = message.answer.call_args.args[0]
    assert "вы уже верифицированы" in called_text.lower() or "verified" in called_text.lower()


@pytest.mark.asyncio
async def test_verification_start_prompts_recording_when_not_verified(monkeypatch):
    # Prepare a fake profile not verified
    fake_profile = SimpleNamespace(verification_status=SimpleNamespace(value="UNVERIFIED"))

    async def fake_get_profile(self, user_id: int):
        return fake_profile

    monkeypatch.setattr(ProfileService, "get_profile", fake_get_profile)

    message = SimpleNamespace(from_user=SimpleNamespace(id=8), answer=AsyncMock())
    state = SimpleNamespace(set_state=AsyncMock())

    await verification_start(message, state, session=None)

    # Should set FSM state to waiting_video and prompt for recording
    state.set_state.assert_called_once_with(VerificationState.waiting_video)
    message.answer.assert_called_once()
    called_text = message.answer.call_args.args[0]
    assert "видеосообщение" in called_text.lower() or "video" in called_text.lower()
