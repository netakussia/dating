from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, TelegramObject

from services.profile_service import ProfileService
from states.appeal import AppealState

logger = logging.getLogger(__name__)


class ProfileRequiredMiddleware(BaseMiddleware):
    """Stops profile-only actions in one place and offers registration."""

    message_actions = {
        "💘 Знакомства", "💘 Смотреть анкеты", "Смотреть анкеты",
        "💕 Мои симпатии", "❤️ Симпатии",
        "🛡 Верификация", "Верификация профиля", "💌 Признание",
        "Посмотреть анкеты", "Показать анкеты", "Открыть анкеты",
        "👤 Моя анкета", "Моя анкета"
    }
    callback_prefixes = (
        "like:", "comment:", "skip:", "block:", "report:", "report_reason:",
        "profile:", "verify:", "photo:"
    )

    @classmethod
    def _requires_profile(cls, event: TelegramObject) -> bool:
        if isinstance(event, Message):
            return (event.text or "") in cls.message_actions
        if isinstance(event, CallbackQuery):
            data = event.data or ""
            return data != "profile:create" and data.startswith(cls.callback_prefixes)
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
        # Prefer the synchronized DB user set by UserSyncMiddleware; fall back to event.from_user
        current_user = data.get("current_user")
        session = data.get("session")
        user_id = None
        if current_user is not None:
            # current_user is a DB model with an `id` attribute
            user_id = getattr(current_user, "id", None)
        else:
            # Prefer an explicit event_from_user in data (some middlewares set this), then event.from_user
            event_user = data.get("event_from_user") or getattr(event, "from_user", None)
            if event_user is not None:
                user_id = getattr(event_user, "id", None)
        # If we don't have session or user id, let the handler run (can't enforce)
        from_user = getattr(event, "from_user", None)
        from_user_id = getattr(from_user, "id", None) if from_user is not None else None
        logger.debug(
            "ProfileRequiredMiddleware invoked: event_type=%s, current_user_id=%s, from_user_id=%s, session_present=%s",
            type(event).__name__, getattr(current_user, "id", None), from_user_id, session is not None,
        )
        if user_id is None or session is None:
            logger.debug("ProfileRequiredMiddleware: insufficient context, passing through")
            return await handler(event, data)
        state = data.get("state")
        current_state = await state.get_state() if state is not None else None
        if isinstance(event, Message) and (
            (event.text or "") == "🆘 Апелляция" or current_state == AppealState.enter_text.state
        ):
            return await handler(event, data)
        # If the profile exists, continue; otherwise prompt to create one
        profile = await ProfileService(session).get_profile(user_id)
        logger.debug("ProfileRequiredMiddleware: profile lookup for user_id=%s -> %s", user_id, bool(profile))
        if profile:
            return await handler(event, data)
        text = "📝 Для начала нужно создать анкету.\n\nБез неё мы не сможем подобрать подходящих людей."
        if isinstance(event, CallbackQuery):
            await event.answer()
            await event.message.answer(text, reply_markup=self._keyboard())
        else:
            await event.answer(text, reply_markup=self._keyboard())
        return None
