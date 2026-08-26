from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from models import UserStatus
from repositories.user import UserRepository
from states.appeal import AppealState


class UserSyncMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[..., Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        session = data.get("session")
        if user and session:
            db_user = await UserRepository(session).get_or_create(user.id, user.username)
            if db_user.status == UserStatus.BANNED:
                state = data.get("state")
                current_state = await state.get_state() if state is not None else None
                appeal_allowed = isinstance(event, Message) and (
                    (event.text or "") == "🆘 Апелляция" or current_state == AppealState.enter_text.state
                )
                if appeal_allowed:
                    data["current_user"] = db_user
                    return await handler(event, data)
                if isinstance(event, CallbackQuery):
                    await event.answer("🚫 Ваш аккаунт заблокирован. Доступ к боту ограничен.", show_alert=True)
                elif isinstance(event, Message):
                    await event.answer("🚫 Ваш аккаунт заблокирован. Доступ к боту ограничен.")
                return None
            data["current_user"] = db_user
        return await handler(event, data)
