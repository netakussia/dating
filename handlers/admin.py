import uuid

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from keyboards.admin import admin_keyboard, appeal_keyboard, moderation_keyboard
from models import AppealStatus, ReportStatus, UserStatus
from repositories.appeal import AppealRepository
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
        profile = await ProfileRepository(session).by_user_id(report.target_user_id)
        profile_info = "Анкета не найдена"
        if profile:
            profile_info = f"{profile.name}, {profile.age}; {profile.district}; {profile.institution}\n{profile.bio}"
        await callback.message.answer(
            f"Жалоба #{report.id}\nПользователь: <code>{report.target_user_id}</code>\n"
            f"Причина: {report.reason.value}\nДетали: {report.details or 'не указаны'}\n\nАнкета:\n{profile_info}",
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
            profile.moderation_locked = True
        user = await UserRepository(session).get(report.target_user_id)
        if user:
            user.status = UserStatus.SUSPENDED
        await repo.resolve(report_id, ReportStatus.APPROVED)
        await callback.bot.send_message(
            report.target_user_id,
            "⏸ Ваша анкета временно приостановлена модерацией. Вы можете нажать «🆘 Апелляция» и описать ситуацию.",
        )
        result = "Анкета приостановлена и скрыта. Пользователю предложена апелляция."
    else:
        await repo.resolve(report_id, ReportStatus.DISMISSED)
        result = "Жалоба отклонена."
    await callback.message.edit_text(f"✅ {result}")
    await callback.answer()


@router.callback_query(F.data == "admin:appeals")
async def appeals(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    items = await AppealRepository(session).pending()
    if not items:
        await callback.message.answer("Открытых апелляций нет.")
    else:
        appeal = items[0]
        await callback.message.answer(
            f"⚖️ Апелляция #{appeal.id}\nПользователь: <code>{appeal.user_id}</code>\n\n{appeal.text}",
            reply_markup=appeal_keyboard(str(appeal.id)),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("appeal:"))
async def appeal_action(callback: CallbackQuery, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    _, action, raw_id = callback.data.split(":")
    try:
        appeal_id = uuid.UUID(raw_id)
    except ValueError:
        await callback.answer("Некорректная апелляция", show_alert=True)
        return
    repo = AppealRepository(session)
    appeal = await repo.get(appeal_id)
    if appeal is None or appeal.status != AppealStatus.PENDING:
        await callback.answer("Апелляция уже обработана", show_alert=True)
        return
    if action == "reply":
        await state.update_data(appeal_id=str(appeal_id), appeal_user_id=appeal.user_id)
        await state.set_state(AdminState.appeal_reply)
        await callback.message.answer("Введите ответ пользователю. Он будет отправлен от имени администрации.")
        await callback.answer()
        return
    if action == "restore":
        user = await UserRepository(session).get(appeal.user_id)
        profile = await ProfileRepository(session).by_user_id(appeal.user_id)
        if user:
            user.status = UserStatus.ACTIVE
        if profile:
            profile.moderation_locked = False
        await repo.resolve(appeal_id, AppealStatus.RESOLVED, callback.from_user.id)
        await callback.bot.send_message(appeal.user_id, "✅ Апелляция одобрена. Ограничение снято; при желании включите видимость анкеты.")
        result = "Апелляция одобрена, аккаунт восстановлен."
    else:
        await repo.resolve(appeal_id, AppealStatus.REJECTED, callback.from_user.id)
        await callback.bot.send_message(appeal.user_id, "❌ Апелляция отклонена. Анкета остаётся приостановленной.")
        result = "Апелляция отклонена."
    await callback.message.edit_text(f"✅ {result}")
    await callback.answer()


@router.message(AdminState.appeal_reply)
async def appeal_reply(message: Message, state: FSMContext, settings: Settings) -> None:
    if not allowed(message.from_user.id, settings):
        await state.clear()
        return
    text = (message.text or "").strip()
    if not 1 <= len(text) <= 4000:
        await message.answer("Ответ должен содержать от 1 до 4000 символов.")
        return
    data = await state.get_data()
    await message.bot.send_message(data["appeal_user_id"], f"⚖️ Ответ администрации:\n\n{text}")
    await state.clear()
    await message.answer("✅ Ответ отправлен. Апелляция остаётся в очереди до решения.")


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
