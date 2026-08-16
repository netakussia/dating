import logging
import time

from aiogram import Bot

logger = logging.getLogger(__name__)


class NotificationService:
    _recent_alerts: dict[tuple[int, str], float] = {}

    def __init__(self, bot: Bot) -> None: self.bot = bot

    async def safe_send(
        self,
        user_id: int,
        text: str,
        *,
        dedupe_key: str | None = None,
        dedupe_window_seconds: int = 1800,
    ) -> bool:
        if dedupe_key:
            cache_key = (user_id, dedupe_key)
            now = time.monotonic()
            last_sent = self._recent_alerts.get(cache_key)
            if last_sent is not None and now - last_sent < dedupe_window_seconds:
                return False
            self._recent_alerts[cache_key] = now
        try:
            await self.bot.send_message(user_id, text)
            return True
        except Exception:
            logger.warning("Telegram notification delivery failed", extra={"user_id": user_id}, exc_info=True)
            return False
