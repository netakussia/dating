from types import SimpleNamespace

import pytest
from sqlalchemy.exc import IntegrityError

from models import ReportReason, UserStatus
from repositories.report import ReportRepository


class FakeResult:
    def __init__(self, row):
        self._row = row

    def one_or_none(self):
        return self._row


class FakeSavepoint:
    async def __aenter__(self):
        return self

    async def __aexit__(self, _exc_type, _exc, _traceback):
        return False


class FakeReportSession:
    def __init__(self, *, existing=None, report_count=2):
        self.existing = existing
        self.profile = SimpleNamespace(report_count=report_count, is_visible=True, moderation_locked=False)
        self.target_profile = self.profile
        self.user = SimpleNamespace(status=UserStatus.ACTIVE)
        self.added = []
        self.scalar_calls = 0
        self.executed_updates = []

    async def scalar(self, _statement):
        self.scalar_calls += 1
        if self.scalar_calls == 1:
            return self.existing
        return self.target_profile

    async def execute(self, statement):
        self.executed_updates.append(statement)
        if len(self.executed_updates) == 1:
            self.profile.report_count += 1
            return FakeResult(
                SimpleNamespace(
                    report_count=self.profile.report_count,
                    user_id=2,
                    is_visible=True,
                    moderation_locked=False,
                )
            )
        if len(self.executed_updates) == 2:
            self.profile.is_visible = False
            self.profile.moderation_locked = True
            return FakeResult(None)
        if len(self.executed_updates) == 3:
            self.user.status = UserStatus.SUSPENDED
            return FakeResult(None)
        return FakeResult(None)

    async def get(self, _model, _key):
        return self.user

    def add(self, item):
        self.added.append(item)

    def begin_nested(self):
        return FakeSavepoint()

    async def flush(self):
        return None


class FakeDuplicateReportSession(FakeReportSession):
    def __init__(self):
        super().__init__(existing=None, report_count=2)
        self.rollback_called = False
        self.existing = SimpleNamespace(reporter_id=1, target_user_id=2)

    async def scalar(self, _statement):
        self.scalar_calls += 1
        if self.scalar_calls == 1:
            return None
        return self.existing

    async def flush(self):
        raise IntegrityError("duplicate key value violates unique constraint", {}, None)


@pytest.mark.asyncio
async def test_report_threshold_hides_profile_and_suspends_user():
    session = FakeReportSession(report_count=2)

    _, created, threshold_reached = await ReportRepository(session).add(1, 2, ReportReason.SPAM, threshold=3)

    assert created and threshold_reached
    assert session.added[0].target_user_id == 2
    assert len(session.executed_updates) == 3
    assert not session.target_profile.is_visible
    assert session.target_profile.moderation_locked
    assert session.user.status == UserStatus.SUSPENDED


@pytest.mark.asyncio
async def test_duplicate_report_does_not_increment_report_count_or_raise():
    session = FakeDuplicateReportSession()

    existing_report, created, threshold_reached = await ReportRepository(session).add(
        1,
        2,
        ReportReason.SPAM,
        threshold=3,
    )

    assert not created
    assert not threshold_reached
    assert existing_report is not None


@pytest.mark.asyncio
async def test_report_above_threshold_does_not_repeat_suspension_side_effects():
    session = FakeReportSession(report_count=3)

    _, created, threshold_reached = await ReportRepository(session).add(1, 2, ReportReason.SPAM, threshold=3)

    assert created
    assert not threshold_reached
    assert len(session.executed_updates) == 1
