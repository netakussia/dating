import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiogram.exceptions import TelegramBadRequest

from config import Settings
from keyboards.admin import admin_keyboard
from models import UserRole
from services.notification_service import InternalNotificationService, NotificationService
from utils.admin_roles import can_manage_admins, can_review_moderator_decisions, resolve_admin_role
from utils.admin_ui import admin_role_label, compact_display_id, user_display_name


class FakeBot:
    def __init__(self):
        self.sent = []

    async def send_message(self, chat_id, text, **kwargs):
        self.sent.append((chat_id, text, kwargs))


class FailingBot:
    async def send_message(self, *_args, **_kwargs):
        raise RuntimeError("telegram down")


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


def test_admin_permission_hierarchy_is_explicit_and_safe():
    assert resolve_admin_role(100, owner_admin_id=100, admin_ids={100, 200}) == UserRole.OWNER
    assert resolve_admin_role(200, owner_admin_id=100, admin_ids={100, 200}) == UserRole.MODERATOR
    assert can_manage_admins(UserRole.OWNER)
    assert not can_manage_admins(UserRole.MODERATOR)
    assert can_review_moderator_decisions(UserRole.CHIEF_MODERATOR)
    assert not can_review_moderator_decisions(UserRole.MODERATOR)


def test_backend_role_hierarchy_blocks_forbidden_admin_actions():
    assert not can_review_moderator_decisions(UserRole.MODERATOR)
    assert not can_manage_admins(UserRole.MODERATOR)
    assert not can_manage_admins(UserRole.HEAD_MODERATOR)


def test_admin_menu_includes_profile_browse_action():
    markup = admin_keyboard()
    callback_ids = {
        button.callback_data
        for row in markup.inline_keyboard
        for button in row
        if getattr(button, "callback_data", None)
    }
    assert "admin:browse" in callback_ids


def test_admin_browse_next_nav_uses_current_profile_id():
    from keyboards.admin import admin_nav_keyboard, profile_moderation_keyboard

    markup = profile_moderation_keyboard(999, "admin:browse:next:999")
    callback_ids = {
        button.callback_data
        for row in markup.inline_keyboard
        for button in row
        if getattr(button, "callback_data", None)
    }
    assert "admin:browse:next:999" in callback_ids
    assert "profilemod:prompt:ban:999" in callback_ids

    nav = admin_nav_keyboard("admin:browse:next:999")
    assert "admin:browse:next:999" in {
        button.callback_data
        for row in nav.inline_keyboard
        for button in row
        if getattr(button, "callback_data", None)
    }


def test_photo_case_requires_an_explicit_atomic_claim_before_decision():
    from keyboards.admin import case_decision_keyboard, case_keyboard

    callbacks = {
        button.callback_data
        for row in case_keyboard("case-id").inline_keyboard
        for button in row
    }
    assert "case:claim:case-id" in callbacks
    decisions = {
        button.callback_data
        for row in case_decision_keyboard("case-id").inline_keyboard
        for button in row
    }
    assert "case:reject:case-id" in decisions


@pytest.mark.asyncio
async def test_notification_service_deduplicates_repeated_admin_alerts():
    bot = FakeBot()
    service = NotificationService(bot)

    first = await service.safe_send(777, "alert", dedupe_key="verification:abc")
    second = await service.safe_send(777, "alert", dedupe_key="verification:abc")

    assert first is True
    assert second is False
    assert len(bot.sent) == 1


@pytest.mark.asyncio
async def test_internal_notification_service_is_disabled_without_chat_id():
    settings = Settings(bot_token="x" * 30, daily_secret_salt="y" * 20, meanima_internal_chat_id=None)
    bot = FakeBot()
    service = InternalNotificationService(bot, settings)

    assert service.enabled is False
    assert await service.send_event("bugs", "hello") is False
    assert bot.sent == []


def test_internal_chat_accepts_short_environment_name(monkeypatch):
    monkeypatch.setenv("MEANIMA_INTERNAL_CHAT", "42")
    settings = Settings(_env_file=None, bot_token="x" * 30, daily_secret_salt="y" * 20)

    assert settings.meanima_internal_chat_id == 42


@pytest.mark.asyncio
async def test_internal_notification_service_sends_to_forum_thread():
    settings = Settings(
        bot_token="x" * 30,
        daily_secret_salt="y" * 20,
        meanima_internal_chat_id=42,
        meanima_internal_errors_thread_id=7,
    )
    bot = FakeBot()
    service = InternalNotificationService(bot, settings)

    sent = await service.send_event("errors", "oops", thread_id=7)

    assert sent is True
    assert bot.sent[0][0] == 42
    assert bot.sent[0][2]["message_thread_id"] == 7


@pytest.mark.asyncio
async def test_notification_service_failure_does_not_break_main_operation():
    service = NotificationService(FailingBot())

    assert await service.safe_send(123, "alert") is False
    assert await service.safe_send(456, "other") is False


@pytest.mark.asyncio
async def test_leaving_admin_administration_clears_broadcast_state(monkeypatch):
    from handlers.admin import section_administration

    monkeypatch.setattr("handlers.admin._require_admin_capability", AsyncMock(return_value=True))
    monkeypatch.setattr("handlers.admin._safe_edit_message_text", AsyncMock())
    callback = SimpleNamespace(answer=AsyncMock(), from_user=SimpleNamespace(id=1), message=SimpleNamespace())
    state = SimpleNamespace(clear=AsyncMock())
    settings = SimpleNamespace()

    await section_administration(callback, session=SimpleNamespace(), settings=settings, state=state)

    state.clear.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("callback_data", "expected"),
    [
        ("mycase:verify:request", "mycase:verify:request"),
        ("mycase:case:case", "mycase:case:case"),
        ("mycase:report:report", "mycase:report:report"),
        ("mycase:appeal:appeal", "mycase:appeal:appeal"),
    ],
)
async def test_moderation_notification_uses_case_specific_callback(callback_data, expected):
    from services.notification_service import InternalNotificationService

    settings = Settings(
        bot_token="x" * 30,
        daily_secret_salt="y" * 20,
        meanima_internal_chat_id=42,
    )
    bot = FakeBot()

    await InternalNotificationService(bot, settings).send_moderation_event(
        "moderation event", case_id=callback_data, target_callback=callback_data, event_key=callback_data
    )

    markup = bot.sent[0][2]["reply_markup"]
    assert markup.inline_keyboard[0][0].callback_data == expected


@pytest.mark.asyncio
async def test_admin_browse_fetches_one_profile_at_a_time():
    from handlers.admin import _next_browse_user

    class Session:
        def __init__(self):
            self.queries = []

        async def scalar(self, statement):
            self.queries.append(statement)
            return SimpleNamespace(id=20)

    session = Session()

    target = await _next_browse_user(session, current_user_id=10)

    assert target.id == 20
    assert len(session.queries) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("case_type", ["NSFW", "NO_FACE"])
async def test_photo_queue_accepts_supported_case_types(monkeypatch, case_type):
    from handlers.admin import _show_next_photo_case
    from models import ModerationCaseType
    from repositories.trust import TrustRepository

    item = SimpleNamespace(case_type=getattr(ModerationCaseType, case_type))
    monkeypatch.setattr(TrustRepository, "pending_cases", AsyncMock(return_value=[item]))
    render_photo_case = AsyncMock()
    monkeypatch.setattr("handlers.admin._render_photo_case", render_photo_case)
    callback = SimpleNamespace(message=SimpleNamespace(delete=AsyncMock()), from_user=SimpleNamespace(id=1))

    await _show_next_photo_case(callback, SimpleNamespace())

    callback.message.delete.assert_awaited_once()
    render_photo_case.assert_awaited_once_with(callback, SimpleNamespace(), item)


@pytest.mark.asyncio
async def test_internal_notification_disables_after_chat_not_found():
    settings = Settings(
        bot_token="x" * 30,
        daily_secret_salt="y" * 20,
        meanima_internal_chat_id=42,
    )

    class ChatMissingBot:
        def __init__(self):
            self.calls = 0

        async def send_message(self, **kwargs):
            self.calls += 1
            raise TelegramBadRequest(method="sendMessage", message="Bad Request: chat not found")

    bot = ChatMissingBot()
    service = InternalNotificationService(bot, settings)

    # first failure should not immediately disable notifications (transient)
    assert await service.send_event("moderation", "oops") is False
    assert service.enabled is True
    assert bot.calls == 1

    # after threshold failures, notifications become disabled
    threshold = service._CHAT_NOT_FOUND_DISABLE_AFTER
    for _ in range(threshold - 1):
        assert await service.send_event("moderation", "oops") is False

    assert service.enabled is False
    assert bot.calls == threshold


def test_admin_section_keyboards_structure_and_callbacks():
    from keyboards.admin import (
        admin_administration_keyboard,
        admin_moderation_keyboard,
        admin_nav_keyboard,
        admin_stats_keyboard,
        admin_users_keyboard,
        my_cases_keyboard,
    )

    mod_cb = {
        btn.callback_data
        for row in admin_moderation_keyboard().inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {
        "admin:reports",
        "admin:nsfw",
        "admin:verifications",
        "admin:appeals",
        "admin:my_cases",
        "admin:menu",
    }.issubset(mod_cb)

    users_cb = {
        btn.callback_data
        for row in admin_users_keyboard().inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {"admin:browse", "admin:blocked", "admin:menu"}.issubset(users_cb)

    stats_cb = {
        btn.callback_data
        for row in admin_stats_keyboard(can_view_history=True).inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {"admin:trust_stats", "admin:trust_history", "admin:menu"}.issubset(stats_cb)

    admin_cb = {
        btn.callback_data
        for row in admin_administration_keyboard().inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {"admin:broadcast", "admin:menu"}.issubset(admin_cb)

    my_cases_markup = my_cases_keyboard([("Кейс 1", "mycase:report:123")])
    my_cases_cb = {
        btn.callback_data
        for row in my_cases_markup.inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {"mycase:report:123", "admin:my_cases", "admin:section:moderation", "admin:menu"}.issubset(my_cases_cb)

    nav = admin_nav_keyboard(
        next_callback="next:1",
        back_callback="back:1",
        refresh_callback="refresh:1",
        prev_callback="prev:1",
    )
    nav_cb = {
        btn.callback_data
        for row in nav.inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {"next:1", "back:1", "refresh:1", "prev:1", "admin:menu"}.issubset(nav_cb)


def test_profile_moderation_keyboard_roles_and_states():
    from keyboards.admin import profile_moderation_keyboard

    # Active user, ordinary moderator cannot unban
    active_markup = profile_moderation_keyboard(123, is_banned=False, is_frozen=False, can_unban=False)
    active_cbs = {
        btn.callback_data
        for row in active_markup.inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert "profilemod:prompt:ban:123" in active_cbs
    assert "profilemod:prompt:freeze:123" in active_cbs

    # Suspended user, admin with can_unban
    frozen_markup = profile_moderation_keyboard(123, is_banned=False, is_frozen=True, can_unban=True)
    frozen_cbs = {
        btn.callback_data
        for row in frozen_markup.inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert "profilemod:prompt:unfreeze:123" in frozen_cbs
    assert "profilemod:prompt:ban:123" in frozen_cbs

    # Banned user, admin with can_unban
    banned_markup = profile_moderation_keyboard(123, is_banned=True, is_frozen=False, can_unban=True)
    banned_cbs = {
        btn.callback_data
        for row in banned_markup.inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert "profilemod:prompt:unban:123" in banned_cbs
