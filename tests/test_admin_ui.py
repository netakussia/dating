import uuid

import pytest

from services.notification_service import NotificationService
from utils.admin_ui import admin_role_label, compact_display_id, user_display_name


class FakeBot:
    def __init__(self):
        self.sent = []

    async def send_message(self, chat_id, text):
        self.sent.append((chat_id, text))


def test_compact_display_id_shortens_queue_ids_for_moderation_ui():
    report_id = uuid.UUID("12345678-1234-4234-8234-123456789abc")

    assert compact_display_id(report_id) == "12345678"
    assert compact_display_id(123456789) == "456789"


def test_admin_role_label_uses_owner_and_moderator_tiers():
    assert admin_role_label(100, username="alice", owner_admin_id=100) == "👑 Netakussia — владелец"
    assert admin_role_label(200, username="alice") == "⚔️ @alice — модератор"
    assert admin_role_label(300, username=None) == "⚔️ модератор — модератор"


def test_user_display_name_hides_the_full_telegram_id():
    assert user_display_name(123456789, username="alice") == "@alice"
    assert user_display_name(123456789).startswith("#")
    assert len(user_display_name(123456789)) <= 8


@pytest.mark.asyncio
async def test_notification_service_deduplicates_repeated_admin_alerts():
    bot = FakeBot()
    service = NotificationService(bot)

    first = await service.safe_send(777, "alert", dedupe_key="verification:abc")
    second = await service.safe_send(777, "alert", dedupe_key="verification:abc")

    assert first is True
    assert second is False
    assert len(bot.sent) == 1
