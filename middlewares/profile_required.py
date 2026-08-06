from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, TelegramObject

from services.profile_service import ProfileService


class ProfileRequiredMiddleware(BaseMiddleware):
    """Stops profile-only actions in one place and offers registration."""

    message_actions = {
        "💘 Знакомства", "💘 Смотреть анкеты", "Смотреть анкеты",
        "💕 Мои симпатии", "❤️ Симпатии",
        "🛡 Верификация", "💌 Признание"
    }
    callback_prefixes = (
        "like:", "comment:", "skip:", "block:", "report:", "report_reason:",
        "profile:toggle", "profile:pause", "profile:delete", "profile:photos", "photo:"
    )

    @classmethod
    def _requires_profile(cls, event: TelegramObject) -> bool:
        if isinstance(event, Message):
            return (event.text or "") in cls.message_actions
        if isinstance(event, CallbackQuery):
            return (event.data or "").startswith(cls.callback_prefixes)
        return False

    @staticmethod
    def _keyboard() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="✨ Создать анкету", callback_data="profile:create")]]
        )

    async def __call__(
        self, handler: Callable[..., Awaitable[Any]], event: TelegramObject, data: dict[str, Any]
    ) -> Any:
        if not self._requires_profile(event):
            return await handler(event, data)
        user = data.get("event_from_user")
        session = data.get("session")
        if user is None or session is None or await ProfileService(session).get_profile(user.id):
            return await handler(event, data)
        text = "📝 Для начала нужно создать анкету.\n\nБез неё мы не сможем подобрать подходящих людей."
        if isinstance(event, CallbackQuery):
            await event.answer()
            await event.message.answer(text, reply_markup=self._keyboard())
        else:
            await event.answer(text, reply_markup=self._keyboard())
        return None
