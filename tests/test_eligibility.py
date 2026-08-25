from types import SimpleNamespace

import pytest

from handlers.dating import _target_id
from models import ModerationStatus, ReportReason, UserStatus
from repositories.discovery import DiscoveryRepository
from services.like_service import LikeService
from services.report_service import ReportService


class FakeEligibilitySession:
    def __init__(self, *, profile=None, user=None, block=None):
        self._scalar_results = [profile, block]
        self.user = user
        self.added = []

    async def scalar(self, _statement):
        if not self._scalar_results:
            return None
        return self._scalar_results.pop(0)

    async def get(self, _model, _key):
        return self.user

    def add(self, item):
        self.added.append(item)

    async def flush(self):
        return None


@pytest.mark.asyncio
async def test_like_service_rejects_ineligible_targets():
    profile = SimpleNamespace(
        user_id=2,
        is_visible=False,
        moderation_locked=False,
        moderation_status=ModerationStatus.CLEAR,
    )
    user = SimpleNamespace(status=UserStatus.ACTIVE)
    session = FakeEligibilitySession(profile=profile, user=user)

    with pytest.raises(ValueError, match="Анкета недоступна"):
        await LikeService(session).create(1, 2)


@pytest.mark.asyncio
async def test_report_service_rejects_inactive_users():
    profile = SimpleNamespace(
        user_id=2,
        is_visible=True,
        moderation_locked=False,
        moderation_status=ModerationStatus.CLEAR,
    )
    user = SimpleNamespace(status=UserStatus.PAUSED)
    session = FakeEligibilitySession(profile=profile, user=user)

    with pytest.raises(ValueError, match="Анкета недоступна"):
        await ReportService(session, threshold=3).submit(1, 2, ReportReason.SPAM)


@pytest.mark.asyncio
async def test_block_repository_skips_ineligible_target_without_persisting_block():
    profile = SimpleNamespace(
        user_id=2,
        is_visible=True,
        moderation_locked=False,
        moderation_status=ModerationStatus.CLEAR,
    )
    user = SimpleNamespace(status=UserStatus.ACTIVE)
    session = FakeEligibilitySession(profile=profile, user=user, block=1)

    created = await DiscoveryRepository(session).block(1, 2)

    assert created is False
    assert session.added == []


@pytest.mark.asyncio
async def test_block_repository_reports_when_block_is_created():
    profile = SimpleNamespace(
        user_id=2,
        is_visible=True,
        moderation_locked=False,
        moderation_status=ModerationStatus.CLEAR,
    )
    user = SimpleNamespace(status=UserStatus.ACTIVE)
    session = FakeEligibilitySession(profile=profile, user=user, block=None)

    created = await DiscoveryRepository(session).block(1, 2)

    assert created is True
    assert len(session.added) == 1


def test_legacy_callback_data_still_parses_target_id():
    assert _target_id(SimpleNamespace(data="comment:42")) == 42
