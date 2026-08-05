import logging

from aiogram import Bot

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, bot: Bot) -> None: self.bot = bot
    async def safe_send(self, user_id: int, text: str) -> bool:
        try:
            await self.bot.send_message(user_id, text)
            return True
        except Exception:
            logger.warning("Telegram notification delivery failed", extra={"user_id": user_id}, exc_info=True)
            return False
