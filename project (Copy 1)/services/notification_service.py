from aiogram import Bot

class NotificationService:
    def __init__(self, bot: Bot) -> None: self.bot = bot
    async def safe_send(self, user_id: int, text: str) -> bool:
        try:
            await self.bot.send_message(user_id, text)
            return True
        except Exception:
            return False
