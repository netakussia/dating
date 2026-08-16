from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from models import UserStatus
from repositories.appeal import AppealRepository
from repositories.trust import TrustRepository
from repositories.user import UserRepository
from services.notification_service import NotificationService
from states.appeal import AppealState
from utils.admin_ui import compact_display_id, user_display_name
from utils.document_links import documents_keyboard

router = Router()


@router.message(F.text == "🆘 Апелляция")
async def appeal_start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    user = await UserRepository(session).get(message.from_user.id)
    if user is None or user.status not in {UserStatus.SUSPENDED, UserStatus.BANNED}:
        await message.answer(
            "⚠️ Апелляция доступна только после ограничения или блокировки анкеты."
        )
        return
    await state.set_state(AppealState.enter_text)
    await message.answer(
        "🆘 Апелляция\nОпишите ситуацию для модератора в свободной форме (20–1500 символов).\n\n"
        "Перед подачей можно быстро ознакомиться с правилами сообщества и процессом апелляции:",
        reply_markup=documents_keyboard("community", "moderation", "safety"),
    )


@router.message(AppealState.enter_text)
async def appeal_send(message: Message, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    text = (message.text or "").strip()
    if not 20 <= len(text) <= 1500:
        await message.answer("⚠️ Текст должен быть от 20 до 1500 символов.")
        return
    appeal = await AppealRepository(session).create(message.from_user.id, text)
    await state.clear()
    notifier = NotificationService(message.bot)
    for admin_id in settings.admin_ids:
        await notifier.safe_send(
            admin_id,
            (
                f"⚖️ Новая апелляция {compact_display_id(appeal.id)}\n"
                f"Пользователь: {user_display_name(appeal.user_id)}\n\n{text[:400]}"
            ),
            dedupe_key=f"appeal:{appeal.id}",
        )
        await TrustRepository(session).log(
            admin_id,
            "appeal_notice_sent",
            target_type="appeal",
            target_id=str(appeal.id),
            metadata={"user_id": appeal.user_id},
        )
    await message.answer(
        "✅ Апелляция отправлена. Модератор свяжется с вами через бот после проверки."
    )
