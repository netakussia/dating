from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query()
async def outdated_callback(callback: CallbackQuery) -> None:
    """Acknowledge buttons retained in old Telegram messages after UI changes."""
    await callback.answer("Эта кнопка устарела. Откройте актуальный раздел меню.", show_alert=True)
