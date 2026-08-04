from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from models import UserStatus
from repositories.appeal import AppealRepository
from repositories.user import UserRepository
from states.appeal import AppealState

router = Router()


@router.message(F.text == "🆘 Апелляция")
async def appeal_start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    user = await UserRepository(session).get(message.from_user.id)
    if user is None or user.status != UserStatus.SUSPENDED:
        await message.answer("Апелляция доступна только для приостановленной анкеты.")
        return
    await state.set_state(AppealState.enter_text)
    await message.answer("Опишите ситуацию для модератора (20–1500 символов).")


@router.message(AppealState.enter_text)
async def appeal_send(message: Message, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    text = (message.text or "").strip()
    if not 20 <= len(text) <= 1500:
        await message.answer("Текст должен быть от 20 до 1500 символов.")
        return
    appeal = await AppealRepository(session).create(message.from_user.id, text)
    await state.clear()
    for admin_id in settings.admin_ids:
        await message.bot.send_message(
            admin_id,
            f"⚖️ Новая апелляция #{appeal.id}\nПользователь: <code>{appeal.user_id}</code>\n\n{text}",
        )
    await message.answer("✅ Апелляция отправлена. Администратор сможет ответить вам в боте.")
