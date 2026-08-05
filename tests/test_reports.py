from types import SimpleNamespace

import pytest

from models import ReportReason, UserStatus
from repositories.report import ReportRepository


class FakeReportSession:
    def __init__(self, *, existing=None, report_count=2):
        self.existing = existing
        self.profile = SimpleNamespace(report_count=report_count, is_visible=True, moderation_locked=False)
        self.target_profile = self.profile
        self.user = SimpleNamespace(status=UserStatus.ACTIVE)
        self.added = []
        self.scalar_calls = 0

    async def scalar(self, _statement):
        self.scalar_calls += 1
        if self.scalar_calls == 1:
            return self.existing
        return self.target_profile

    async def get(self, _model, _key):
        return self.user

    def add(self, item):
        self.added.append(item)

    async def flush(self):
        return None


@pytest.mark.asyncio
async def test_report_threshold_hides_profile_and_suspends_user():
    session = FakeReportSession(report_count=2)

    _, created, threshold_reached = await ReportRepository(session).add(1, 2, ReportReason.SPAM, threshold=3)

    assert created and threshold_reached
    assert session.added[0].target_user_id == 2
    assert not session.target_profile.is_visible
    assert session.target_profile.moderation_locked
    assert session.user.status == UserStatus.SUSPENDED
