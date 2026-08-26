import asyncio
import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from config import Settings
from handlers.admin import _render_report
from models import ReportReason, ReportStatus
from services.notification_service import NotificationService
from services.report_service import ReportService


class FakeRedis:
    def __init__(self):
        self.values = {}

    async def exists(self, key):
        return key in self.values

    async def set(self, key, value, *, nx=False, ex=None):
        if nx and key in self.values:
            return False
        self.values[key] = value
        return True

    async def delete(self, key):
        self.values.pop(key, None)


class FakeBot:
    def __init__(self, redis=None, *, fail=False):
        self.notification_redis = redis
        self.fail = fail
        self.sent = []

    async def send_message(self, chat_id, text, **kwargs):
        if self.fail:
            raise RuntimeError("telegram unavailable")
        self.sent.append((chat_id, text, kwargs))


class BrokenRedis:
    async def exists(self, _key):
        raise RuntimeError("redis unavailable")

    async def set(self, *_args, **_kwargs):
        raise RuntimeError("redis unavailable")


class CleanupBrokenRedis(FakeRedis):
    async def delete(self, _key):
        raise RuntimeError("redis unavailable")


class FakeMessage:
    def __init__(self):
        self.sent = []

    async def answer(self, text, **kwargs):
        self.sent.append((text, kwargs))

    async def answer_photo(self, _photo, *, caption, **kwargs):
        self.sent.append((caption, kwargs))


class FakeSession:
    async def get(self, _model, _user_id):
        return SimpleNamespace(username="target")


def test_confession_and_fsm_settings_have_safe_defaults():
    settings = Settings(bot_token="x" * 30, daily_secret_salt="y" * 20)

    assert settings.confession_daily_limit == 20
    assert settings.confession_pending_ttl_hours == 168
    assert settings.fsm_state_ttl_seconds == 3600


@pytest.mark.asyncio
async def test_report_snapshot_survives_profile_change_and_is_rendered():
    profile = SimpleNamespace(
        name="Before",
        age=22,
        district="Center",
        institution="University",
        bio="Original bio",
        interests=["music"],
        photo_file_ids=["photo-before"],
        main_photo_file_id="photo-before",
    )
    snapshot = ReportService._evidence_snapshot(profile)
    profile.name, profile.bio, profile.photo_file_ids = "After", "Changed", []

    report = SimpleNamespace(
        id=uuid.uuid4(),
        evidence_snapshot=snapshot,
        target_user_id=42,
        reason=ReportReason.FAKE,
        details=None,
        status=ReportStatus.PENDING,
        assigned_to=None,
        created_at=datetime.now(UTC),
    )
    message = FakeMessage()
    callback = SimpleNamespace(message=message, from_user=SimpleNamespace(id=7))

    await _render_report(callback, FakeSession(), report)

    assert snapshot["name"] == "Before"
    assert snapshot["photo_file_ids"] == ["photo-before"]
    assert "Before, 22" in message.sent[0][0]


@pytest.mark.asyncio
async def test_redis_notification_dedupe_survives_new_service_and_retries_failure():
    redis = FakeRedis()
    bot = FakeBot(redis)
    first = NotificationService(bot)
    restarted = NotificationService(bot)

    assert await first.safe_send(42, "event", dedupe_key="event:1") is True
    assert await restarted.safe_send(42, "event", dedupe_key="event:1") is False
    assert len(bot.sent) == 1

    failing = FakeBot(redis, fail=True)
    assert await NotificationService(failing).safe_send(43, "event", dedupe_key="event:2") is False
    retry = FakeBot(redis)
    assert await NotificationService(retry).safe_send(43, "event", dedupe_key="event:2") is True


@pytest.mark.asyncio
async def test_redis_notification_concurrent_duplicates_send_once():
    redis = FakeRedis()
    bot = FakeBot(redis)
    results = await asyncio.gather(
        NotificationService(bot).safe_send(42, "event", dedupe_key="concurrent"),
        NotificationService(bot).safe_send(42, "event", dedupe_key="concurrent"),
    )

    assert results.count(True) == 1
    assert len(bot.sent) == 1


@pytest.mark.asyncio
async def test_redis_dedupe_failure_does_not_abort_notification():
    bot = FakeBot(BrokenRedis())

    assert await NotificationService(bot).safe_send(42, "event", dedupe_key="outage") is True
    assert len(bot.sent) == 1


@pytest.mark.asyncio
async def test_successful_notification_survives_redis_cleanup_failure():
    bot = FakeBot(CleanupBrokenRedis())

    assert await NotificationService(bot).safe_send(42, "event", dedupe_key="cleanup") is True
    assert len(bot.sent) == 1
