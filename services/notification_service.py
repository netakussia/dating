import logging
import re
import time
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from config import Settings, get_settings

logger = logging.getLogger(__name__)


def _truncate_text(value: str | None, max_length: int = 4000) -> str:
    if value is None:
        return ""
    cleaned = value.strip()
    if len(cleaned) <= max_length:
        return cleaned
    return cleaned[: max_length - 3].rstrip() + "..."


def _redact_sensitive(value: str | None) -> str:
    if not value:
        return ""
    redacted = re.sub(
        r"(?i)(token|password|secret|api[_-]?key|authorization)\s*[:=]\s*[^\s,\n]+",
        r"\1=[REDACTED]",
        value,
    )
    redacted = re.sub(
        r"(?i)(BOT_TOKEN|MEANIMA_INTERNAL_CHAT_ID|MEANIMA_INTERNAL_\w+_THREAD_ID)\s*[:=]\s*[^\s,\n]+",
        r"\1=[REDACTED]",
        redacted,
    )
    return redacted


class NotificationService:
    _recent_alerts: dict[tuple[int, str], float] = {}

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def _acquire_delivery(self, key: str, window: int) -> tuple[bool, str | None]:
        """Shared Redis idempotency lock; falls back only for legacy tests."""
        redis = getattr(self.bot, "notification_redis", None)
        if redis is None:
            return True, None
        delivered, lock = f"notification:delivered:{key}", f"notification:lock:{key}"
        if await redis.exists(delivered):
            return False, None
        # A short lease makes a worker crash retryable; delivery is marked only
        # after Telegram accepted the message.
        if not await redis.set(lock, "1", nx=True, ex=60):
            return False, None
        return True, lock

    async def _finish_delivery(self, key: str, lock: str | None, *, success: bool, window: int) -> None:
        redis = getattr(self.bot, "notification_redis", None)
        if redis is None or lock is None:
            return
        if success:
            await redis.set(f"notification:delivered:{key}", "1", ex=window)
        await redis.delete(lock)

    async def safe_send(
        self,
        user_id: int,
        text: str,
        *,
        reply_markup: InlineKeyboardMarkup | None = None,
        dedupe_key: str | None = None,
        dedupe_window_seconds: int = 1800,
    ) -> bool:
        shared_key = f"{user_id}:{dedupe_key}" if dedupe_key else None
        lock = None
        if shared_key:
            try:
                acquired, lock = await self._acquire_delivery(shared_key, dedupe_window_seconds)
            except Exception:
                logger.warning("Notification dedupe unavailable; sending without Redis lock.", exc_info=True)
                shared_key = None
                lock = None
            else:
                if not acquired:
                    return False
        if dedupe_key and getattr(self.bot, "notification_redis", None) is None:
            cache_key = (user_id, dedupe_key)
            now = time.monotonic()
            last_sent = self._recent_alerts.get(cache_key)
            if last_sent is not None and now - last_sent < dedupe_window_seconds:
                return False
        try:
            await self.bot.send_message(user_id, text, reply_markup=reply_markup)
        except Exception:
            if shared_key:
                try:
                    await self._finish_delivery(shared_key, lock, success=False, window=dedupe_window_seconds)
                except Exception:
                    logger.warning("Notification dedupe cleanup failed after delivery error.", exc_info=True)
            logger.warning("Telegram notification delivery failed", extra={"user_id": user_id}, exc_info=True)
            return False
        if dedupe_key and getattr(self.bot, "notification_redis", None) is None:
            self._recent_alerts[(user_id, dedupe_key)] = time.monotonic()
        if shared_key:
            try:
                await self._finish_delivery(shared_key, lock, success=True, window=dedupe_window_seconds)
            except Exception:
                logger.warning("Notification dedupe cleanup failed after successful delivery.", exc_info=True)
        return True


class InternalNotificationService:
    _recent_alerts: dict[tuple[str, str], float] = {}
    _sending_error_notification = False
    # how many consecutive "chat not found" errors before we disable notifications
    _CHAT_NOT_FOUND_DISABLE_AFTER = 3

    def __init__(self, bot: Bot, settings: Settings | None = None) -> None:
        self.bot = bot
        self.settings = settings or get_settings()
        self._disabled_by_chat = False
        # Counter for consecutive chat-not-found errors. Reset on success.
        self._consecutive_chat_not_found = 0

    @property
    def enabled(self) -> bool:
        return bool(self.settings.meanima_internal_chat_id) and not self._disabled_by_chat

    def _thread_id_for(self, kind: str) -> int | None:
        threads: Mapping[str, int | None] = {
            "bugs": self.settings.meanima_internal_bug_thread_id,
            "moderation": self.settings.meanima_internal_moderation_thread_id,
            "errors": self.settings.meanima_internal_errors_thread_id,
            "stats": self.settings.meanima_internal_stats_thread_id,
        }
        return threads.get(kind)

    async def send_event(
        self,
        kind: str,
        text: str,
        *,
        thread_id: int | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        dedupe_key: str | None = None,
        dedupe_window_seconds: int = 1800,
    ) -> bool:
        if not self.enabled:
            return False
        if kind == "errors" and self._sending_error_notification:
            logger.warning("Skipping recursive internal error notification.")
            return False
        if dedupe_key:
            cache_key = (kind, dedupe_key)
            now = time.monotonic()
            last_sent = self._recent_alerts.get(cache_key)
            if last_sent is not None and now - last_sent < dedupe_window_seconds:
                return False

        target_thread = thread_id if thread_id is not None else self._thread_id_for(kind)
        chat_id = self.settings.meanima_internal_chat_id
        payload = {
            "chat_id": chat_id,
            "text": _truncate_text(_redact_sensitive(text), 4096),
        }
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup

        attempt_payloads = [payload]
        if target_thread is not None:
            attempt_payloads = [{**payload, "message_thread_id": target_thread}, payload]

        # Diagnostic log: what we are attempting to send (redact only sensitive content already applied to text)
        try:
            logger.debug(
                "Attempting internal notification",
                extra={
                    "chat_id": int(chat_id) if chat_id is not None else None,
                    "message_thread_id": int(target_thread) if target_thread is not None else None,
                    "kind": kind,
                },
            )
        except Exception:
            # Avoid any accidental logging of unexpected objects — fall back to safe message
            logger.debug("Attempting internal notification for kind=%s", kind)

        last_error: Exception | None = None
        for attempt in attempt_payloads:
            try:
                if kind == "errors":
                    self.__class__._sending_error_notification = True
                await self.bot.send_message(**attempt)
                if dedupe_key:
                    # A failed Telegram request must remain retryable.  This
                    # mirrors user notifications' success-only dedupe rule.
                    self._recent_alerts[(kind, dedupe_key)] = time.monotonic()
                # Success — reset chat-not-found counter
                self._consecutive_chat_not_found = 0
                return True
            except TelegramBadRequest as exc:
                last_error = exc
                msg = str(exc).lower()
                # A broken, closed, or unavailable forum topic must not swallow
                # the notification: retry in the main group without a thread.
                if target_thread is not None and ("message thread" in msg or "topic" in msg):
                    logger.warning(
                        "Internal Telegram notification topic is invalid for %s; retrying without thread_id.",
                        kind,
                        exc_info=True,
                    )
                    # don't mark chat as unavailable; try fallback (next iteration)
                    continue

                # Chat not found or invalid chat id — increment counter and disable only after threshold
                if "chat not found" in msg or "chat_id is invalid" in msg or "not found" in msg:
                    # increment counter and log diagnostic without exposing secrets
                    self._consecutive_chat_not_found += 1
                    logger.warning(
                        "Internal Telegram chat reported 'chat not found' for kind=%s (chat_id=%s)."
                        " Consecutive missing count=%d/%d.",
                        kind,
                        str(chat_id),
                        self._consecutive_chat_not_found,
                        self._CHAT_NOT_FOUND_DISABLE_AFTER,
                        exc_info=False,
                    )
                    if self._consecutive_chat_not_found >= self._CHAT_NOT_FOUND_DISABLE_AFTER:
                        self._disabled_by_chat = True
                        logger.exception(
                            "Internal Telegram chat unavailable for %s; disabling after %d failed attempts",
                            kind,
                            self._consecutive_chat_not_found,
                        )
                        return False
                    # Do not disable yet — allow future attempts
                    return False

                # Other TelegramBadRequest — treat as permanent for now
                logger.exception("Internal Telegram notification delivery failed for %s", kind)
                return False
            except Exception as exc:
                last_error = exc
                logger.exception("Internal Telegram notification delivery failed for %s", kind)
                return False
            finally:
                if kind == "errors":
                    self.__class__._sending_error_notification = False

        if last_error is not None:
            logger.exception("Internal Telegram notification delivery failed for %s", kind)
        return False

    async def send_bug_report(
        self,
        user_id: int,
        *,
        username: str | None,
        description: str,
        context: str | None = None,
    ) -> bool:
        user_label = f"@{username}" if username else "без username"
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        lines = [
            "🐛 BUG REPORT",
            "",
            f"👤 User: {user_label}",
            f"🆔 ID: {user_id}",
            f"🕐 Time: {timestamp}",
            "",
            "📝 Description:",
            _truncate_text(description, 1800),
        ]
        if context:
            lines.extend(["", "Контекст:", _truncate_text(context, 600)])
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Открыть кейс", callback_data="admin:reports")]]
        )
        return await self.send_event("bugs", "\n".join(lines), reply_markup=markup, dedupe_key=f"bug:{user_id}")

    async def send_moderation_event(
        self,
        title: str,
        *,
        user_id: int | None = None,
        username: str | None = None,
        reason: str | None = None,
        case_id: str | None = None,
        details: str | None = None,
        photo_file_ids: Sequence[str] | None = None,
        event_key: str | None = None,
        target_callback: str | None = None,
    ) -> bool:
        user_label = f"@{username}" if username else "без username" if user_id is not None else "—"
        lines = ["🚩 MODERATION", "", title]
        if user_id is not None:
            lines.append(f"User: {user_label}")
            lines.append(f"ID: {user_id}")
        if reason:
            lines.append(f"Reason: {reason}")
        if case_id:
            lines.append(f"Case: {case_id}")
        if details:
            lines.append("")
            lines.append(_truncate_text(details, 600))
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Открыть кейс", callback_data=target_callback or "admin:reports")
            ]]
        )
        text = "\n".join(lines)
        if photo_file_ids:
            photo_ids = [photo for photo in photo_file_ids if photo][:3]
            if photo_ids:
                media = [
                    InputMediaPhoto(media=photo_id, caption=text if index == 0 else None)
                    for index, photo_id in enumerate(photo_ids)
                ]
                try:
                    if hasattr(self.bot, "send_media_group"):
                        await self.bot.send_media_group(
                            chat_id=self.settings.meanima_internal_chat_id,
                            media=media,
                            message_thread_id=self._thread_id_for("moderation"),
                        )
                    else:
                        await self.bot.send_photo(
                            chat_id=self.settings.meanima_internal_chat_id,
                            photo=photo_ids[0],
                            caption=text,
                            message_thread_id=self._thread_id_for("moderation"),
                        )
                except Exception:
                    logger.warning("Failed to send moderation photos for internal moderation event.", exc_info=True)
                return await self.send_event(
                    "moderation",
                    text,
                    reply_markup=markup,
                    dedupe_key=f"moderation:{event_key or case_id or user_id or title}",
                )
        return await self.send_event(
            "moderation",
            text,
            reply_markup=markup,
            dedupe_key=f"moderation:{event_key or case_id or user_id or title}",
        )

    async def send_error_notification(
        self,
        *,
        module: str,
        exception_type: str,
        message: str,
        traceback_text: str | None,
    ) -> bool:
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        lines = [
            "⚠️ APPLICATION ERROR",
            "",
            f"🕐 {timestamp}",
            f"📍 {module}",
            "",
            "Exception:",
            exception_type,
            "",
            "Message:",
            _truncate_text(_redact_sensitive(message), 800),
            "",
            "Traceback:",
            _truncate_text(_redact_sensitive(traceback_text or ""), 1800),
        ]
        return await self.send_event("errors", "\n".join(lines), dedupe_key="error:system")

    async def send_daily_stats(self, stats: Mapping[str, int | float]) -> bool:
        lines = [
            "📊 DAILY STATS",
            "",
            f"👤 New users: {stats.get('new_users', 0)}",
            f"📝 New profiles: {stats.get('new_profiles', 0)}",
            f"❤️ Likes: {stats.get('likes', 0)}",
            f"💞 Matches: {stats.get('matches', 0)}",
            f"🚩 Reports: {stats.get('reports', 0)}",
            f"🛡 Moderation cases: {stats.get('moderation_cases', 0)}",
            f"✅ Verifications: {stats.get('verifications', 0)}",
        ]
        return await self.send_event("stats", "\n".join(lines), dedupe_key="stats:daily")
