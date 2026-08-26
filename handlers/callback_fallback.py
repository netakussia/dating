from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from keyboards.menu import main_menu

router = Router()


@router.callback_query()
async def outdated_callback(callback: CallbackQuery) -> None:
    """Acknowledge buttons retained in old Telegram messages after UI changes."""
    await callback.answer("Эта кнопка устарела. Откройте актуальный раздел меню.", show_alert=True)


@router.message(StateFilter(None))
async def no_state_message(message: Message) -> None:
    await message.answer(
        "Я не нашёл активного действия для этого сообщения. Откройте нужный раздел меню.",
        reply_markup=main_menu(),
    )
