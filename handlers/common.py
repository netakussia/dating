import uuid
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.menu import main_menu
from services.confession_service import ConfessionService

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, session: AsyncSession, settings) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) == 2 and args[1].startswith("confession_"):
        try:
            confession = await ConfessionService(session, settings.daily_secret_salt).claim(uuid.UUID(args[1].removeprefix("confession_")), message.from_user.id)
            if confession: await message.answer(f"💌 Вам анонимное признание:\n\n{confession.text}")
        except ValueError: pass
    await state.clear()
    await message.answer("Добро пожаловать! Создайте анкету или найдите симпатию.", reply_markup=main_menu())

@router.message(Command("help"))
@router.message(lambda m: m.text == "❓ Помощь")
async def help_(message: Message, settings) -> None:
    support_lines = []
    for admin_id in settings.admin_ids:
        support_lines.append(f"<a href=\"tg://user?id={admin_id}\">Админ #{admin_id}</a>")
    support = "\n".join(support_lines) if support_lines else "Служба поддержки не настроена."
    await message.answer(
        "Создайте анкету через «Моя анкета», затем откройте «Знакомства». Признания отправляются анонимно.\n\n"
        f"Если нужна помощь, напишите одному из администраторов:\n{support}"
    )
