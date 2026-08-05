from types import SimpleNamespace

import pytest

from models import ModerationCaseType, ModerationStatus, UserStatus, VerificationStatus
from services.moderation_service import ModerationService
from services.photo_moderation_service import PhotoAssessment, PhotoModerationService


class FakeSession:
    def __init__(self, user=None, profile=None):
        self.user = user
        self.profile = profile
        self.added = []
        self.scalar_values = []

    async def get(self, _model, _id):
        return self.user

    async def scalar(self, _query):
        if self.scalar_values:
            return self.scalar_values.pop(0)
        return self.profile

    def add(self, value):
        self.added.append(value)

    async def flush(self):
        return None


class UnsafeProvider:
    async def assess(self, _photo_id):
        return PhotoAssessment(nsfw_score=0.99, face_detected=False, provider="test")


class FailingProvider:
    async def assess(self, _photo_id):
        raise RuntimeError("model unavailable")


@pytest.mark.asyncio
async def test_ban_and_unban_are_idempotent():
    user = SimpleNamespace(status=UserStatus.ACTIVE)
    profile = SimpleNamespace(is_visible=True, moderation_locked=False, moderation_status=ModerationStatus.CLEAR)
    session = FakeSession(user, profile)
    service = ModerationService(session)

    assert await service.ban(7, 99, reason="test")
    assert user.status == UserStatus.BANNED
    assert not profile.is_visible and profile.moderation_locked
    assert not await service.ban(7, 99, reason="test")
    assert await service.unban(7, 99)
    assert user.status == UserStatus.ACTIVE
    assert not await service.unban(7, 99)


@pytest.mark.asyncio
async def test_nsfw_and_no_face_open_manual_review_case():
    profile = SimpleNamespace(
        moderation_status=ModerationStatus.CLEAR,
        is_visible=True,
        moderation_locked=False,
    )
    session = FakeSession(profile=profile)
    session.scalar_values = [profile, None]
    assessment = await PhotoModerationService(session, nsfw_threshold=0.85, provider=UnsafeProvider()).inspect(
        7, "photo"
    )

    assert assessment.nsfw_score == 0.99
    assert not assessment.face_detected
    assert profile.moderation_status == ModerationStatus.UNDER_REVIEW
    assert not profile.is_visible and profile.moderation_locked
    assert any(getattr(item, "case_type", None) == ModerationCaseType.NSFW for item in session.added)


def test_new_profile_defaults_are_unverified():
    assert VerificationStatus.UNVERIFIED.value == "UNVERIFIED"


@pytest.mark.asyncio
async def test_photo_provider_failure_hides_profile_and_opens_review_case():
    from services.photo_moderation_service import PhotoModerationError

    profile = SimpleNamespace(
        moderation_status=ModerationStatus.CLEAR,
        is_visible=True,
        moderation_locked=False,
    )
    session = FakeSession(profile=profile)
    session.scalar_values = [profile, None]

    with pytest.raises(PhotoModerationError):
        await PhotoModerationService(session, nsfw_threshold=0.85, provider=FailingProvider()).inspect(7, "photo")

    assert profile.moderation_status == ModerationStatus.UNDER_REVIEW
    assert not profile.is_visible and profile.moderation_locked
    assert any(getattr(item, "case_type", None) == ModerationCaseType.NSFW for item in session.added)
