from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from models import (
    AppealStatus,
    ModerationCaseStatus,
    ModerationCaseType,
    ModerationStatus,
    UserRole,
    UserStatus,
    VerificationStatus,
)
from repositories.trust import TrustRepository
from services.moderation_service import ModerationService
from services.photo_moderation_service import PhotoAssessment, PhotoModerationService
from services.profile_service import ProfileService
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

    async def fake_get(model, _id):
        if model.__name__ == "User" and _id == 99:
            return SimpleNamespace(role=UserRole.OWNER)
        return user

    session.get = fake_get

    assert await service.ban(7, 99, reason="test")
    assert user.status == UserStatus.BANNED
    assert not profile.is_visible and profile.moderation_locked
    assert not await service.ban(7, 99, reason="test")
    assert await service.unban(7, 99)
    assert user.status == UserStatus.ACTIVE
    assert not await service.unban(7, 99)


@pytest.mark.asyncio
async def test_approve_appeal_restores_user_profile_and_marks_appeal():
    user = SimpleNamespace(status=UserStatus.SUSPENDED, role=UserRole.OWNER)
    profile = SimpleNamespace(
        is_visible=False,
        moderation_locked=True,
        moderation_status=ModerationStatus.UNDER_REVIEW,
    )
    appeal = SimpleNamespace(user_id=7, id="appeal-1", status=AppealStatus.PENDING, admin_id=None)

    class AppealSession:
        async def get(self, _model, _identity):
            return user

        async def scalar(self, _query):
            return profile

        async def execute(self, _query):
            return SimpleNamespace(scalars=lambda: SimpleNamespace(first=lambda: None))

        def add(self, _value):
            return None

        async def flush(self):
            return None

    service = ModerationService(AppealSession())
    service.repo.log = AsyncMock()

    restored, reason = await service.restore_appeal_sanction(appeal, 99, actor_role=UserRole.OWNER)

    assert (restored, reason) == (True, None)
    assert user.status == UserStatus.ACTIVE
    assert profile.is_visible is True
    assert profile.moderation_locked is False
    assert profile.moderation_status == ModerationStatus.CLEAR
    assert appeal.status == AppealStatus.APPROVED
    service.repo.log.assert_awaited_once()


@pytest.mark.asyncio
async def test_moderator_cannot_ban_self():
    user = SimpleNamespace(status=UserStatus.ACTIVE, role=UserRole.MODERATOR)

    class SelfBanSession:
        async def get(self, model, item_id):
            if model.__name__ == "User":
                return user if item_id == 7 else SimpleNamespace(role=UserRole.MODERATOR)
            return None

        async def scalar(self, _query):
            return None

        async def flush(self):
            return None

    service = ModerationService(SelfBanSession())

    assert await service.ban(7, 7, reason="self-ban") is False


@pytest.mark.asyncio
async def test_case_claim_wins_and_wrong_owner_cannot_resolve():
    case = SimpleNamespace(
        id="case-1",
        user_id=7,
        case_type=ModerationCaseType.NSFW,
        status=ModerationCaseStatus.PENDING,
        assigned_to=None,
        assigned_at=None,
        admin_id=None,
    )

    class ClaimSession:
        def __init__(self, case_ref):
            self.case_ref = case_ref

        async def get(self, model, item_id):
            if model.__name__ == "User":
                if item_id == 101:
                    return SimpleNamespace(role=UserRole.MODERATOR)
                if item_id == 202:
                    return SimpleNamespace(role=UserRole.MODERATOR)
                return None
            if model.__name__ == "ModerationCase":
                return self.case_ref
            return None

        async def scalar(self, _query):
            return None

        async def flush(self):
            return None

        def add(self, _value):
            return None

        async def execute(self, _query):
            self.case_ref.status = ModerationCaseStatus.IN_PROGRESS
            self.case_ref.assigned_to = 101
            self.case_ref.assigned_at = "now"
            return SimpleNamespace(scalar_one_or_none=lambda: self.case_ref)

    session = ClaimSession(case)
    service = ModerationService(session)

    claimed_case, claimed, _ = await service.claim_case(case.id, 101)
    assert claimed is True
    assert claimed_case.assigned_to == 101
    assert claimed_case.status == ModerationCaseStatus.IN_PROGRESS

    resolved_case, changed, resolution = await service.resolve_case(case.id, 202)
    assert changed is False
    assert resolution in {"already_assigned", "forbidden"}
    assert resolved_case.assigned_to == 101


@pytest.mark.asyncio
async def test_moderator_cannot_resolve_or_ban_other_claimed_case():
    case = SimpleNamespace(
        id="case-2",
        user_id=7,
        case_type=ModerationCaseType.NSFW,
        status=ModerationCaseStatus.IN_PROGRESS,
        assigned_to=101,
        assigned_at=None,
        admin_id=None,
    )

    class PermissionSession:
        async def get(self, model, item_id):
            if model.__name__ == "User":
                return SimpleNamespace(role=UserRole.MODERATOR)
            if model.__name__ == "ModerationCase":
                return case
            return None

        async def scalar(self, _query):
            return None

        async def flush(self):
            return None

        def add(self, _value):
            return None

        async def execute(self, _query):
            return SimpleNamespace(scalar_one_or_none=lambda: None)

    service = ModerationService(PermissionSession())

    resolved_case, changed, resolution = await service.resolve_case(case.id, 202)
    assert changed is False
    assert resolution == "forbidden"
    assert resolved_case.assigned_to == 101

    assert await service.ban(7, 202, reason="test") is False


@pytest.mark.asyncio
async def test_resolved_case_cannot_be_reprocessed_by_stale_callback():
    case = SimpleNamespace(
        id="case-3",
        user_id=7,
        case_type=ModerationCaseType.NSFW,
        status="RESOLVED",
        assigned_to=101,
        assigned_at=None,
        admin_id=101,
    )

    class ResolvedSession:
        async def get(self, model, _item_id):
            if model.__name__ == "User":
                return SimpleNamespace(role=UserRole.MODERATOR)
            if model.__name__ == "ModerationCase":
                return case
            return None

        async def scalar(self, _query):
            return None

        async def flush(self):
            return None

        def add(self, _value):
            return None

        async def execute(self, _query):
            return SimpleNamespace(scalar_one_or_none=lambda: None)

    service = ModerationService(ResolvedSession())
    resolved_case, changed, resolution = await service.resolve_case(case.id, 101)
    assert changed is False
    assert resolution in {"already_resolved", "not_in_progress"}
    assert resolved_case is case


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
async def test_frozen_profile_remains_frozen_after_safe_photo_assessment():
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

    assert profile.moderation_status == ModerationStatus.UNDER_REVIEW
    assert profile.is_visible is False
    assert profile.moderation_locked is True


@pytest.mark.asyncio
async def test_frozen_profile_remains_frozen_after_photo_update_actions():
    profile = SimpleNamespace(
        user_id=7,
        photo_file_ids=["old-1", "old-2"],
        extra_data={"photo_file_ids": ["old-1", "old-2"]},
        moderation_status=ModerationStatus.UNDER_REVIEW,
        is_visible=False,
        moderation_locked=True,
    )
    session = FakeSession(profile=profile)
    session.scalar_values = [profile]

    service = ProfileService(session)
    updated_add = await service.add_photo(7, "new-3")
    updated_replace = await service.replace_photo(7, "old-1", "new-1")
    updated_remove = await service.remove_photo(7, "old-2")

    assert updated_add.moderation_locked is True
    assert updated_replace.moderation_locked is True
    assert updated_remove.moderation_locked is True
    assert updated_add.is_visible is False
    assert updated_replace.is_visible is False
    assert updated_remove.is_visible is False


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
        open_verification=AsyncMock(return_value=(SimpleNamespace(user_id=7, video_file_id="video-file"), True)),
    )

    request = await service.submit(7, "video-file")

    assert profile.verification_status == VerificationStatus.PENDING
    assert request.video_file_id == "video-file"
