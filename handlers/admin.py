import uuid

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from keyboards.admin import admin_keyboard, appeal_keyboard, case_keyboard, moderation_keyboard, verification_keyboard
from models import AppealStatus, ModerationCaseType, ReportStatus, User, UserStatus, VerificationDecision
from repositories.appeal import AppealRepository
from repositories.profile import ProfileRepository
from repositories.report import ReportRepository
from repositories.trust import TrustRepository
from repositories.user import UserRepository
from services.matching_debug import MatchingDebugService
from services.moderation_service import ModerationService
from services.notification_service import NotificationService
from services.report_service import ReportService
from services.trust_stats_service import TrustStatsService
from services.verification_service import VerificationService
from states.admin import AdminState

router = Router()


def allowed(user_id: int, settings: Settings) -> bool:
    return user_id in settings.admin_ids


@router.message(Command("admin"))
async def admin(message: Message, settings: Settings) -> None:
    if not allowed(message.from_user.id, settings):
        return
    await message.answer("Панель модерации", reply_markup=admin_keyboard())


@router.message(Command("debug_matching"))
async def debug_matching(message: Message, session: AsyncSession, settings: Settings) -> None:
    if not allowed(message.from_user.id, settings):
        return
    report = await MatchingDebugService(session, weights=settings.matching_weights).report_for(message.from_user.id)
    excluded = [item for item in report.candidates if not item.included]
    lines = [
        "<b>Matching debug</b>",
        f"Пользователей: {report.stats.users}; активных: {report.stats.active_users}",
        f"Просмотров: {report.stats.views}; лайков: {report.stats.likes}; матчей: {report.stats.matches}",
        f"CTR: {report.stats.ctr}%; средняя совместимость: {report.stats.average_compatibility}%",
        f"Кандидатов после базовых фильтров: {len(report.candidates)}",
        f"Прошли фильтр пола/цели: {report.gender_compatible}",
        (
            f"Релевантный возраст: {report.age_relevant}; совпали районы: {report.same_district}; "
            f"общие интересы: {report.shared_interests}"
        ),
        f"В очереди: {len(report.candidates) - len(excluded)}",
        "Исключения:",
    ]
    if excluded:
        lines.extend(f"• {item.candidate_id}: {', '.join(item.reasons)}" for item in excluded[:50])
    else:
        lines.append("• нет")
    await message.answer("\n".join(lines))


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


@router.callback_query(F.data == "admin:verifications")
async def verification_queue(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        return
    items = await TrustRepository(session).pending_verifications()
    if not items:
        await callback.message.answer("Очередь верификаций пуста.")
    else:
        item = items[0]
        await callback.message.answer_video_note(item.video_file_id)
        await callback.message.answer(
            f"🛡 Верификация #{item.id}\nПользователь: <code>{item.user_id}</code>",
            reply_markup=verification_keyboard(str(item.id)),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("verify:"))
async def verification_decision(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        return
    try:
        _, action, raw_id = callback.data.split(":")
        decision = {
            "approve": VerificationDecision.APPROVED,
            "reject": VerificationDecision.REJECTED,
            "retake": VerificationDecision.RETAKE_REQUESTED,
        }[action]
        request_id = uuid.UUID(raw_id)
    except (KeyError, ValueError):
        await callback.answer("Некорректное решение", show_alert=True)
        return
    request, changed = await VerificationService(session).decide(request_id, callback.from_user.id, decision)
    if not changed:
        await callback.answer("Верификация уже обработана", show_alert=True)
        return
    messages = {
        VerificationDecision.APPROVED: "🟢 Верификация подтверждена.",
        VerificationDecision.REJECTED: "❌ Верификация отклонена.",
        VerificationDecision.RETAKE_REQUESTED: "🔁 Пожалуйста, запишите кружок ещё раз.",
    }
    await NotificationService(callback.bot).safe_send(request.user_id, messages[decision])
    await callback.message.edit_text(f"✅ Решение сохранено: {decision.value}")
    await callback.answer()


@router.callback_query(F.data == "admin:nsfw")
async def nsfw_queue(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        return
    items = await TrustRepository(session).pending_cases()
    items = [item for item in items if item.case_type in {ModerationCaseType.NSFW, ModerationCaseType.NO_FACE}]
    if not items:
        await callback.message.answer("Очередь NSFW/фото пуста.")
    else:
        item = items[0]
        await callback.message.answer(
            f"🔞 Фото-проверка #{item.id}\nПользователь: <code>{item.user_id}</code>\n{item.details or ''}",
            reply_markup=case_keyboard(str(item.id)),
        )
    await callback.answer()


@router.callback_query(F.data == "admin:blocked")
async def blocked_users(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        return
    users = list((await session.scalars(select(User).where(User.status == UserStatus.BANNED).limit(30))).all())
    if not users:
        await callback.message.answer("Заблокированных пользователей нет.")
    else:
        await callback.message.answer(
            "🚫 Заблокированные:\n" + "\n".join(f"• <code>{user.id}</code>" for user in users)
        )
    await callback.answer()


@router.callback_query(F.data.startswith("case:"))
async def moderation_case(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        return
    try:
        _, action, raw_id = callback.data.split(":")
        case_id = uuid.UUID(raw_id)
    except ValueError:
        await callback.answer("Некорректный кейс", show_alert=True)
        return
    case, changed = await ModerationService(session).resolve_case(
        case_id, callback.from_user.id, restore=action == "restore"
    )
    if not changed:
        await callback.answer("Кейс уже закрыт", show_alert=True)
        return
    await callback.message.edit_text("✅ Фото-проверка закрыта.")
    await callback.answer()


@router.callback_query(F.data == "admin:trust_history")
async def trust_history(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        return
    items = await TrustRepository(session).history()
    lines = ["📜 История Trust"] + [
        f"• {item.created_at:%d.%m %H:%M}: {item.action} → {item.target_id or '—'}" for item in items
    ]
    await callback.message.answer("\n".join(lines[:31]) if items else "История решений пуста.")
    await callback.answer()


@router.callback_query(F.data == "admin:trust_stats")
async def trust_stats(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        return
    stats = await TrustStatsService(session).snapshot()
    await callback.message.answer(
        "📊 Trust статистика\n"
        f"Проверенных: {stats['verified']}\nЖалоб: {stats['reports']}\n"
        f"Ложных жалоб: {stats['false_reports']}\nПодтверждённых фейков: {stats['confirmed_fakes']}\n"
        f"Средний Trust Score: {stats['average_trust_score']}"
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
        await ModerationService(session).ban(report.target_user_id, callback.from_user.id, reason="report")
        await ReportService(session, threshold=settings.report_threshold).confirm_fake(report_id, callback.from_user.id)
        result = "Пользователь заблокирован."
    elif action == "hide":
        await ModerationService(session).suspend(report.target_user_id, callback.from_user.id, reason="report")
        await repo.resolve(report_id, ReportStatus.APPROVED)
        await callback.bot.send_message(
            report.target_user_id,
            "⏸ Ваша анкета временно приостановлена модерацией. Вы можете нажать «🆘 Апелляция» и описать ситуацию.",
        )
        result = "Анкета приостановлена и скрыта. Пользователю предложена апелляция."
    else:
        await ReportService(session, threshold=settings.report_threshold).dismiss(report_id, callback.from_user.id)
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
        await TrustRepository(session).log(
            callback.from_user.id, "appeal_restored", target_type="appeal", target_id=str(appeal_id)
        )
        await callback.bot.send_message(
            appeal.user_id,
            "✅ Апелляция одобрена. Ограничение снято; при желании включите видимость анкеты.",
        )
        result = "Апелляция одобрена, аккаунт восстановлен."
    else:
        await repo.resolve(appeal_id, AppealStatus.REJECTED, callback.from_user.id)
        await TrustRepository(session).log(
            callback.from_user.id, "appeal_rejected", target_type="appeal", target_id=str(appeal_id)
        )
        await callback.bot.send_message(appeal.user_id, "❌ Апелляция отклонена. Анкета остаётся приостановленной.")
        result = "Апелляция отклонена."
    await callback.message.edit_text(f"✅ {result}")
    await callback.answer()


@router.message(AdminState.appeal_reply)
async def appeal_reply(message: Message, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    if not allowed(message.from_user.id, settings):
        await state.clear()
        return
    text = (message.text or "").strip()
    if not 1 <= len(text) <= 4000:
        await message.answer("Ответ должен содержать от 1 до 4000 символов.")
        return
    data = await state.get_data()
    await message.bot.send_message(data["appeal_user_id"], f"⚖️ Ответ администрации:\n\n{text}")
    await TrustRepository(session).log(
        message.from_user.id,
        "appeal_replied",
        target_type="appeal",
        target_id=str(data["appeal_id"]),
    )
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
