from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from repositories.profile import ProfileRepository
from services.localization import LocalizationService

SUPPORTED_LOCALES = {"ru", "ro"}


def normalize_locale(value: str | None) -> str:
    code = (value or "ru").split("-", 1)[0].lower()
    return code if code in SUPPORTED_LOCALES else "ru"


class FSMI18nMiddleware(BaseMiddleware):
    def __init__(self, localizer: LocalizationService | None = None) -> None:
        self.localizer = localizer or LocalizationService()

    async def __call__(
        self,
        handler: Callable[..., Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        telegram_user = data.get("event_from_user")
        locale = normalize_locale(getattr(telegram_user, "language_code", None))
        session = data.get("session")
        if telegram_user is not None and session is not None:
            profile = await ProfileRepository(session).by_user_id(telegram_user.id)
            if profile is not None:
                locale = normalize_locale(profile.locale)
        data["locale"] = locale
        data["localizer"] = self.localizer
        return await handler(event, data)