from __future__ import annotations

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from services.localization import LocalizationService
from services.profile_service import ProfileService
from utils.document_links import documents_keyboard

CONSENT_KEY = "legal_consent"

LEGAL_NOTICE_TEXT = (
    "👋 MeAnima — это сервис знакомств в формате Telegram-бота.\n\n"
    "Это закрытая альфа: часть функциональности ещё дорабатывается, а часть процессов только запускается.\n\n"
    "Перед использованием важно ознакомиться с правилами, политикой конфиденциальности и условиями сервиса.\n\n"
    "Мы используем MeAnima, чтобы знакомиться и общаться в безопасной среде в рамках закрытого тестирования."
)


def legal_notice_text(locale: str = "ru") -> str:
    return LocalizationService().get("legal_notice", locale)


async def consent_already_given(state: FSMContext) -> bool:
    data = await state.get_data()
    return bool(data.get(CONSENT_KEY))


async def ensure_consent_for_new_user(
    state: FSMContext,
    session: AsyncSession,
    user_id: int,
    message: Message | CallbackQuery,
    locale: str = "ru",
) -> bool:
    if await consent_already_given(state):
        return True

    if await ProfileService(session).get_profile(user_id) is not None:
        await state.update_data(**{CONSENT_KEY: True})
        return True

    if isinstance(message, CallbackQuery):
        await message.answer()
        await message.message.answer(
            legal_notice_text(locale),
            reply_markup=documents_keyboard(
                "terms",
                "privacy",
                "community",
                "safety",
                "moderation",
                "alpha",
                include_continue=True,
                locale=locale,
            ),
        )
    else:
        await message.answer(
            legal_notice_text(locale),
            reply_markup=documents_keyboard(
                "terms",
                "privacy",
                "community",
                "safety",
                "moderation",
                "alpha",
                include_continue=True,
                locale=locale,
            ),
        )
    return False


async def accept_consent(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(**{CONSENT_KEY: True})
    await callback.answer()
