import uuid

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from keyboards.admin import admin_keyboard, moderation_keyboard
from models import ReportStatus, UserStatus
from repositories.profile import ProfileRepository
from repositories.report import ReportRepository
from repositories.user import UserRepository
from services.notification_service import NotificationService
from states.admin import AdminState

router = Router()


def allowed(user_id: int, settings: Settings) -> bool:
    return user_id in settings.admin_ids


@router.message(Command("admin"))
async def admin(message: Message, settings: Settings) -> None:
    if not allowed(message.from_user.id, settings):
        return
    await message.answer("Панель модерации", reply_markup=admin_keyboard())


@router.callback_query(F.data == "admin:reports")
async def reports(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    items = await ReportRepository(session).pending()
    if not items:
        await callback.message.answer("Очередь жалоб пуста.")
    else:
        report = items[0]
        await callback.message.answer(
            f"Жалоба #{report.id}\nПользователь: <code>{report.target_user_id}</code>\nПричина: {report.reason.value}",
            reply_markup=moderation_keyboard(str(report.id)),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("moderate:"))
async def moderate(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    _, action, raw_id = callback.data.split(":")
    try:
        report_id = uuid.UUID(raw_id)
    except ValueError:
        await callback.answer("Некорректная жалоба", show_alert=True)
        return
    repo = ReportRepository(session)
    report = await repo.get(report_id)
    if report is None or report.status != ReportStatus.PENDING:
        await callback.answer("Жалоба уже обработана", show_alert=True)
        return
    if action == "ban":
        user = await UserRepository(session).get(report.target_user_id)
        if user:
            user.status = UserStatus.BANNED
        await repo.resolve(report_id, ReportStatus.APPROVED)
        result = "Пользователь заблокирован."
    elif action == "hide":
        profile = await ProfileRepository(session).by_user_id(report.target_user_id)
        if profile:
            profile.is_visible = False
        await repo.resolve(report_id, ReportStatus.APPROVED)
        result = "Анкета скрыта из выдачи."
    else:
        await repo.resolve(report_id, ReportStatus.DISMISSED)
        result = "Жалоба отклонена."
    await callback.message.edit_text(f"✅ {result}")
    await callback.answer()


@router.callback_query(F.data == "admin:broadcast")
async def broadcast_start(callback: CallbackQuery, state: FSMContext, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    await state.set_state(AdminState.broadcast_message)
    await callback.message.answer("Отправьте текст рассылки. Его получат активные пользователи.")
    await callback.answer()


@router.message(AdminState.broadcast_message)
async def broadcast_send(message: Message, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    if not allowed(message.from_user.id, settings):
        await state.clear()
        return
    text = (message.text or "").strip()
    if not 1 <= len(text) <= 4000:
        await message.answer("Текст должен содержать от 1 до 4000 символов.")
        return
    notifier = NotificationService(message.bot)
    delivered = 0
    for user_id in await UserRepository(session).all_ids():
        delivered += await notifier.safe_send(user_id, text)
    await state.clear()
    await message.answer(f"✅ Рассылка завершена. Доставлено: {delivered}.")
