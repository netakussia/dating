from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from models import UserStatus
from repositories.user import UserRepository

class UserSyncMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[..., Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        user = data.get("event_from_user"); session = data.get("session")
        if user and session:
            db_user = await UserRepository(session).get_or_create(user.id, user.username)
            if db_user.status == UserStatus.BANNED: return None
            data["current_user"] = db_user
        return await handler(event, data)
