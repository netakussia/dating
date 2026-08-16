from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from models import ModerationCaseType, ModerationStatus, UserStatus, VerificationStatus
from repositories.trust import TrustRepository
from services.moderation_service import ModerationService
from services.photo_moderation_service import PhotoAssessment, PhotoModerationService
from services.verification_service import VerificationService


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


class SafeProvider:
    async def assess(self, _photo_id):
        return PhotoAssessment(nsfw_score=0.0, face_detected=True, provider="test")


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


@pytest.mark.asyncio
async def test_safe_photo_republishes_profile_only_when_no_pending_case_exists():
    profile = SimpleNamespace(
        moderation_status=ModerationStatus.UNDER_REVIEW,
        is_visible=False,
        moderation_locked=True,
    )
    session = FakeSession(profile=profile)
    session.scalar_values = [profile, None]

    service = PhotoModerationService(session, nsfw_threshold=0.85, provider=SafeProvider())
    service.repo = SimpleNamespace(
        record_photo=AsyncMock(),
        open_case=AsyncMock(return_value=(None, True)),
        pending_cases_for_user=AsyncMock(return_value=[]),
    )

    await service.inspect(7, "photo")

    assert profile.moderation_status == ModerationStatus.CLEAR
    assert profile.is_visible is True
    assert profile.moderation_locked is False


@pytest.mark.asyncio
async def test_trust_repository_does_not_create_duplicate_pending_cases_for_same_event():
    class TrustSession:
        def __init__(self):
            self.added = []
            self._pending = None

        async def scalar(self, _statement):
            return self._pending

        def add(self, item):
            self.added.append(item)
            self._pending = item

        async def flush(self):
            return None

    session = TrustSession()
    repo = TrustRepository(session)

    await repo.open_case(7, ModerationCaseType.NSFW, source_id="hash-1")
    await repo.open_case(7, ModerationCaseType.NSFW, source_id="hash-1")

    assert len(session.added) == 1


@pytest.mark.asyncio
async def test_verification_submit_blocks_verified_and_pending_user():
    profile = SimpleNamespace(verification_status=VerificationStatus.VERIFIED)
    session = FakeSession(profile=profile)
    service = VerificationService(session)
    service.repo = SimpleNamespace(active_verification_for_user=AsyncMock(return_value=None))

    with pytest.raises(ValueError, match="уже верифицированы"):
        await service.submit(7, "video-file")

    profile.verification_status = VerificationStatus.PENDING
    service.repo.active_verification_for_user = AsyncMock(return_value=SimpleNamespace(user_id=7))
    with pytest.raises(ValueError, match="текущая заявка"):
        await service.submit(7, "video-file")


@pytest.mark.asyncio
async def test_verification_submit_accepts_rejected_user_and_sets_pending():
    profile = SimpleNamespace(verification_status=VerificationStatus.REJECTED)
    session = FakeSession(profile=profile)
    service = VerificationService(session)
    service.repo = SimpleNamespace(
        active_verification_for_user=AsyncMock(return_value=None),
        open_verification=AsyncMock(return_value=SimpleNamespace(user_id=7, video_file_id="video-file")),
    )

    request = await service.submit(7, "video-file")

    assert profile.verification_status == VerificationStatus.PENDING
    assert request.video_file_id == "video-file"
