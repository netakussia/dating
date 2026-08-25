from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from models import UserStatus
from repositories.user import UserRepository


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
                if isinstance(event, CallbackQuery):
                    await event.answer("🚫 Ваш аккаунт заблокирован. Доступ к боту ограничен.", show_alert=True)
                elif isinstance(event, Message):
                    await event.answer("🚫 Ваш аккаунт заблокирован. Доступ к боту ограничен.")
                return None
            data["current_user"] = db_user
        return await handler(event, data)
