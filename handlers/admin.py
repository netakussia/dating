import uuid

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from keyboards.admin import (
    admin_administration_keyboard,
    admin_keyboard,
    admin_moderation_keyboard,
    admin_nav_keyboard,
    admin_stats_keyboard,
    admin_users_keyboard,
    appeal_decision_keyboard,
    appeal_keyboard,
    case_decision_keyboard,
    case_keyboard,
    confirm_action_keyboard,
    moderation_decision_keyboard,
    moderation_keyboard,
    my_cases_keyboard,
    profile_moderation_keyboard,
    verification_decision_keyboard,
    verification_keyboard,
)
from models import (
    Appeal,
    AppealStatus,
    ModerationCase,
    ModerationCaseStatus,
    ModerationCaseType,
    ModerationStatus,
    Profile,
    Report,
    ReportStatus,
    User,
    UserRole,
    UserStatus,
    VerificationDecision,
    VerificationRequest,
)
from repositories.appeal import AppealRepository
from repositories.profile import ProfileRepository
from repositories.report import ReportRepository
from repositories.trust import TrustRepository
from repositories.user import UserRepository
from services.matching_debug import MatchingDebugService
from services.moderation_service import ModerationService
from services.notification_service import InternalNotificationService, NotificationService
from services.report_service import ReportService
from services.trust_stats_service import TrustStatsService
from services.verification_service import VerificationService
from states.admin import AdminState
from utils.admin_roles import (
    can_access_moderation,
    can_manage_admins,
    can_override_appeal_assignment,
    can_override_case,
    can_unban,
    can_unfreeze,
    can_view_all_profiles,
    can_view_audit_history,
    resolve_admin_role,
)
from utils.admin_ui import compact_display_id, user_display_name
from utils.profile_media import ordered_photo_ids, send_profile_gallery
from utils.text import escape_html

router = Router()


class _SanctionNotApplied(RuntimeError):
    """Roll back a report decision when its paired sanction cannot be applied."""


def allowed(user_id: int, settings: Settings) -> bool:
    return user_id in settings.admin_ids


def admin_role_for_user(user_id: int, settings: Settings, *, user_role: UserRole | None = None) -> UserRole:
    return resolve_admin_role(
        user_id,
        owner_admin_id=settings.owner_admin_id,
        admin_ids=settings.admin_ids,
        user_role=user_role,
    )


async def _safe_edit_message_text(message: Message, text: str, *, reply_markup=None) -> None:
    try:
        if getattr(message, "photo", None) or getattr(message, "caption", None) is not None:
            await message.edit_caption(caption=text, reply_markup=reply_markup, parse_mode="HTML")
            return
        await message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except TelegramBadRequest as exc:
        msg = str(exc).lower()
        if "message is not modified" in msg or "there is no text in the message to edit" in msg:
            try:
                await message.answer(text, reply_markup=reply_markup, parse_mode="HTML")
            except Exception:
                pass
            return
        if "message to edit not found" in msg or "chat not found" in msg:
            return
        raise


async def _safe_callback_answer(callback: CallbackQuery, text: str | None = None, *, show_alert: bool = False) -> None:
    try:
        await callback.answer(text, show_alert=show_alert)
    except TelegramBadRequest as exc:
        msg = str(exc).lower()
        if any(token in msg for token in ("query is too old", "response timeout expired", "query id is invalid")):
            return
        raise


async def _user_label(session: AsyncSession, user_id: int) -> str:
    user = await session.get(User, user_id)
    return user_display_name(user_id, username=user.username if user else None)


async def _admin_label(session: AsyncSession, admin_id: int | None) -> str:
    if admin_id is None:
        return "не назначен"
    user = await session.get(User, admin_id)
    return user_display_name(admin_id, username=user.username if user else None)


async def _assigned_label(session: AsyncSession, assigned_to: int | None) -> str:
    if assigned_to is None:
        return "не закреплено"
    user = await session.get(User, assigned_to)
    return user_display_name(assigned_to, username=user.username if user else None)


async def _case_label(raw_id: str | uuid.UUID) -> str:
    return f"#{compact_display_id(raw_id)}"


async def _role_for_admin(session: AsyncSession, user_id: int, settings: Settings) -> UserRole:
    """Resolve permissions server-side, rather than trusting Telegram UI state."""
    user = await session.get(User, user_id)
    return admin_role_for_user(user_id, settings, user_role=user.role if user else None)


async def _require_admin_capability(
    callback: CallbackQuery, session: AsyncSession, settings: Settings, capability
) -> bool:
    if not allowed(callback.from_user.id, settings) or not capability(
        await _role_for_admin(session, callback.from_user.id, settings)
    ):
        await callback.answer("Недостаточно прав", show_alert=True)
        return False
    return True


async def _render_report(callback: CallbackQuery, session: AsyncSession, report: Report) -> None:
    snapshot = report.evidence_snapshot or {}
    name = escape_html(snapshot.get("name") or "Не указано")
    age = snapshot.get("age") if snapshot.get("age") is not None else "—"
    district = escape_html(snapshot.get("district") or "Не указано")
    institution = escape_html(snapshot.get("institution") or "Не указано")
    bio = escape_html(snapshot.get("bio") or "Не указано")
    profile_info = f"{name}, {age}; {district}; {institution}\n{bio}"
    photo_ids = [item for item in snapshot.get("photo_file_ids", []) if isinstance(item, str) and item]
    photo_note = f"\nФото на момент жалобы: {len(photo_ids)}"
    target_user = await _user_label(session, report.target_user_id)
    created_str = f"\n📅 Создано: {report.created_at:%d.%m.%Y %H:%M}" if getattr(report, "created_at", None) else ""
    assigned_str = await _assigned_label(session, report.assigned_to)
    caption = (
        f"📢 <b>Жалоба #{compact_display_id(report.id)}</b>\n"
        f"👤 Пользователь: {target_user}\n"
        f"⚠️ Причина: {report.reason.value}\n"
        f"📝 Детали: {escape_html(report.details) if report.details else 'не указаны'}"
        f"{created_str}\n"
        f"📊 Статус: {report.status.value}\n"
        f"👤 Закреплено: {assigned_str}\n\n"
        f"📋 <b>Анкета на момент жалобы:</b>\n{profile_info}{photo_note}"
    )
    if report.assigned_to == callback.from_user.id:
        markup = moderation_decision_keyboard(str(report.id))
    elif report.assigned_to is None:
        markup = moderation_keyboard(str(report.id))
    else:
        markup = admin_nav_keyboard(refresh_callback="admin:reports", back_callback="admin:section:moderation")

    if len(photo_ids) > 1:
        media = [
            InputMediaPhoto(media=photo_id, caption=caption if index == 0 else None, parse_mode="HTML")
            for index, photo_id in enumerate(photo_ids)
        ]
        await callback.message.answer_media_group(media)
        await callback.message.answer("Действие модератора:", reply_markup=markup)
        return
    if photo_ids:
        await callback.message.answer_photo(photo_ids[0], caption=caption, parse_mode="HTML", reply_markup=markup)
        return
    await callback.message.answer(caption, parse_mode="HTML", reply_markup=markup)


async def _show_next_report(callback: CallbackQuery, session: AsyncSession) -> None:
    try:
        await callback.message.delete()
    except Exception:
        pass
    items = await ReportRepository(session).pending(callback.from_user.id)
    if not items:
        await callback.message.answer(
            "📭 Очередь жалоб пуста.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:reports", back_callback="admin:section:moderation"
            ),
        )
        return
    await _render_report(callback, session, items[0])


async def _render_photo_case(callback: CallbackQuery, session: AsyncSession, item: ModerationCase) -> None:
    profile = await ProfileRepository(session).by_user_id(item.user_id)
    created_str = f"\n📅 Создано: {item.created_at:%d.%m.%Y %H:%M}" if getattr(item, "created_at", None) else ""
    assigned_str = await _assigned_label(session, item.assigned_to)
    target_user = await _user_label(session, item.user_id)
    caption = (
        f"🖼️ <b>Фото-проверка #{compact_display_id(item.id)}</b>\n"
        f"👤 Пользователь: {target_user}\n"
        f"⚠️ Тип: {item.case_type.value}\n"
        f"📝 Детали: {escape_html(item.details) if item.details else 'не указаны'}"
        f"{created_str}\n"
        f"📊 Статус: {item.status.value}\n"
        f"👤 Закреплено: {assigned_str}"
    )
    if item.assigned_to == callback.from_user.id:
        markup = case_decision_keyboard(str(item.id))
    elif item.assigned_to is None:
        markup = case_keyboard(str(item.id))
    else:
        markup = admin_nav_keyboard(refresh_callback="admin:nsfw", back_callback="admin:section:moderation")
    photos = ordered_photo_ids(profile) if profile else []
    if photos:
        await send_profile_gallery(callback.message, profile, caption, markup)
        return
    photo = await TrustRepository(session).photo_for_case(item.user_id, item.source_id)
    if photo:
        await callback.message.answer_photo(
            photo.photo_file_id,
            caption=caption,
            parse_mode="HTML",
            reply_markup=markup,
        )
    else:
        await callback.message.answer(
            caption + "\n\n⚠️ Исходное фото недоступно; проверьте детали кейса.",
            parse_mode="HTML",
            reply_markup=markup,
        )


async def _show_next_photo_case(callback: CallbackQuery, session: AsyncSession) -> None:
    try:
        await callback.message.delete()
    except Exception:
        pass
    items = await TrustRepository(session).pending_cases()
    items = [
        item
        for item in items
        if item.case_type
        in {
            ModerationCaseType.NSFW,
            ModerationCaseType.NO_FACE,
            ModerationCaseType.PHOTO_RETAKE,
            ModerationCaseType.ML_PROVIDER_FALLBACK,
        }
    ]
    if not items:
        await callback.message.answer(
            "📭 Очередь фото на проверку пуста.",
            reply_markup=admin_nav_keyboard(refresh_callback="admin:nsfw", back_callback="admin:section:moderation"),
        )
        return
    await _render_photo_case(callback, session, items[0])


async def _render_verification(callback: CallbackQuery, session: AsyncSession, item: VerificationRequest) -> None:
    created_str = f"\n📅 Создано: {item.created_at:%d.%m.%Y %H:%M}" if getattr(item, "created_at", None) else ""
    assigned_str = await _assigned_label(session, item.assigned_to)
    target_user = await _user_label(session, item.user_id)
    text = (
        f"🛡 <b>Верификация #{compact_display_id(item.id)}</b>\n"
        f"👤 Пользователь: {target_user}"
        f"{created_str}\n"
        f"📊 Статус: {item.status.value}\n"
        f"👤 Закреплено: {assigned_str}"
    )
    if item.assigned_to == callback.from_user.id:
        markup = verification_decision_keyboard(str(item.id))
    elif item.assigned_to is None:
        markup = verification_keyboard(str(item.id))
    else:
        markup = admin_nav_keyboard(
            refresh_callback="admin:verifications", back_callback="admin:section:moderation"
        )

    await callback.message.answer_video_note(item.video_file_id)
    await callback.message.answer(text, parse_mode="HTML", reply_markup=markup)


async def _show_next_verification(callback: CallbackQuery, session: AsyncSession) -> None:
    try:
        await callback.message.delete()
    except Exception:
        pass
    items = await TrustRepository(session).pending_verifications()
    if not items:
        await callback.message.answer(
            "📭 Очередь верификаций пуста.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:verifications", back_callback="admin:section:moderation"
            ),
        )
        return
    await _render_verification(callback, session, items[0])


async def _render_appeal(callback: CallbackQuery, session: AsyncSession, appeal: Appeal) -> None:
    created_str = f"\n📅 Создано: {appeal.created_at:%d.%m.%Y %H:%M}" if getattr(appeal, "created_at", None) else ""
    assigned_str = await _assigned_label(session, appeal.assigned_to)
    target_user = await _user_label(session, appeal.user_id)
    text = (
        f"⚖️ <b>Апелляция #{compact_display_id(appeal.id)}</b>\n"
        f"👤 Пользователь: {target_user}"
        f"{created_str}\n"
        f"📊 Статус: {appeal.status.value}\n"
        f"👤 Закреплено: {assigned_str}\n\n"
        f"💬 <b>Текст апелляции:</b>\n{escape_html(appeal.text)}"
    )
    if appeal.assigned_to == callback.from_user.id:
        markup = appeal_decision_keyboard(str(appeal.id))
    elif appeal.assigned_to is None:
        markup = appeal_keyboard(str(appeal.id))
    else:
        markup = admin_nav_keyboard(refresh_callback="admin:appeals", back_callback="admin:section:moderation")

    await callback.message.answer(text, parse_mode="HTML", reply_markup=markup)


async def _show_next_appeal(callback: CallbackQuery, session: AsyncSession, moderator_id: int) -> None:
    try:
        await callback.message.delete()
    except Exception:
        pass
    items = await AppealRepository(session).pending(moderator_id)
    if not items:
        await callback.message.answer(
            "📭 Очередь апелляций пуста.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:appeals", back_callback="admin:section:moderation"
            ),
        )
        return
    await _render_appeal(callback, session, items[0])


async def _render_admin_browse_profile(
    callback: CallbackQuery, session: AsyncSession, target_id: int, actor_role: UserRole
) -> None:
    target = await session.get(User, target_id)
    if target is None:
        await callback.answer("Анкета не найдена.", show_alert=True)
        return
    profile = await ProfileRepository(session).by_user_id(target.id)
    if profile is None:
        await callback.answer("У пользователя нет активной анкеты.", show_alert=True)
        return
    is_banned = target.status == UserStatus.BANNED
    is_frozen = target.status == UserStatus.SUSPENDED
    user_can_unban = can_unban(actor_role)

    caption = (
        f"🔎 <b>Просмотр анкеты</b>\n"
        f"👤 Пользователь: {user_display_name(target.id, username=target.username)}\n"
        f"📊 Статус аккаунта: {target.status.value}\n"
        f"🛡 Модерация анкеты: {profile.moderation_status.value}\n"
        f"🎖 Роль: {target.role.value}\n"
        f"⭐ Trust Score: {target.trust_score}\n\n"
        f"👤 <b>{escape_html(profile.name)}</b>, {profile.age}\n"
        f"📍 Район: {escape_html(profile.district)}\n"
        f"🏫 Учёба/работа: {escape_html(profile.institution)}\n"
        f"📝 О себе: {escape_html(profile.bio or 'Без описания')}"
    )
    markup = profile_moderation_keyboard(
        target.id,
        next_callback=f"admin:browse:next:{target.id}",
        can_unban=user_can_unban,
        is_banned=is_banned,
        is_frozen=is_frozen,
    )
    await send_profile_gallery(callback.message, profile, caption, markup)


async def _next_browse_user(session: AsyncSession, current_user_id: int | None = None) -> User | None:
    statement = select(User).join(Profile).order_by(User.id).limit(1)
    if current_user_id is not None:
        statement = select(User).join(Profile).where(User.id > current_user_id).order_by(User.id).limit(1)
    target = await session.scalar(statement)
    if target is None and current_user_id is not None:
        target = await session.scalar(select(User).join(Profile).order_by(User.id).limit(1))
    return target


@router.message(Command("admin"))
async def admin(message: Message, session: AsyncSession, settings: Settings) -> None:
    if not allowed(message.from_user.id, settings):
        return
    role = await _role_for_admin(session, message.from_user.id, settings)
    await message.answer(
        "🛡 <b>Панель модерации</b>\nВыберите раздел:",
        reply_markup=admin_keyboard(role_can_manage_admins=can_manage_admins(role)),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "admin:menu")
async def admin_menu(callback: CallbackQuery, session: AsyncSession, settings: Settings, state: FSMContext) -> None:
    if not allowed(callback.from_user.id, settings):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    await state.clear()
    role = await _role_for_admin(session, callback.from_user.id, settings)
    await _safe_edit_message_text(
        callback.message,
        "🛡 <b>Панель модерации</b>\nВыберите раздел:",
        reply_markup=admin_keyboard(role_can_manage_admins=can_manage_admins(role)),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:section:moderation")
async def section_moderation(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    await _safe_edit_message_text(
        callback.message,
        "🛡 <b>Раздел модерации</b>\nВыберите категорию для проверки:",
        reply_markup=admin_moderation_keyboard(),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:section:users")
async def section_users(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_view_all_profiles):
        return
    await _safe_edit_message_text(
        callback.message,
        "👤 <b>Управление пользователями</b>\nВыберите действие:",
        reply_markup=admin_users_keyboard(),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:section:stats")
async def section_stats(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    role = await _role_for_admin(session, callback.from_user.id, settings)
    await _safe_edit_message_text(
        callback.message,
        "📊 <b>Статистика и аналитика</b>\nВыберите раздел:",
        reply_markup=admin_stats_keyboard(can_view_history=can_view_audit_history(role)),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:section:administration")
async def section_administration(
    callback: CallbackQuery, session: AsyncSession, settings: Settings, state: FSMContext
) -> None:
    if not await _require_admin_capability(callback, session, settings, can_manage_admins):
        return
    await state.clear()
    await _safe_edit_message_text(
        callback.message,
        "⚙️ <b>Панель администратора</b>\nВыберите действие:",
        reply_markup=admin_administration_keyboard(),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:my_cases")
async def my_cases(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    moderator_id = callback.from_user.id

    my_reports = list(
        (
            await session.scalars(
                select(Report).where(Report.assigned_to == moderator_id, Report.status == ReportStatus.PENDING)
            )
        ).all()
    )
    my_cases_list = list(
        (
            await session.scalars(
                select(ModerationCase).where(
                    ModerationCase.assigned_to == moderator_id,
                    ModerationCase.status == ModerationCaseStatus.IN_PROGRESS,
                )
            )
        ).all()
    )
    my_verifications = list(
        (
            await session.scalars(
                select(VerificationRequest).where(
                    VerificationRequest.assigned_to == moderator_id,
                    VerificationRequest.status == VerificationDecision.PENDING,
                )
            )
        ).all()
    )
    my_appeals = list(
        (
            await session.scalars(
                select(Appeal).where(Appeal.assigned_to == moderator_id, Appeal.status == AppealStatus.PENDING)
            )
        ).all()
    )

    items: list[tuple[str, str]] = []
    for r in my_reports:
        items.append((f"📢 Жалоба #{compact_display_id(r.id)}", f"mycase:report:{r.id}"))
    for c in my_cases_list:
        items.append((f"🖼️ Кейс #{compact_display_id(c.id)}", f"mycase:case:{c.id}"))
    for v in my_verifications:
        items.append((f"🛡 Верификация #{compact_display_id(v.id)}", f"mycase:verify:{v.id}"))
    for a in my_appeals:
        items.append((f"⚖️ Апелляция #{compact_display_id(a.id)}", f"mycase:appeal:{a.id}"))

    total = len(items)
    if total == 0:
        text = "📌 <b>Мои кейсы</b>\n\nУ вас нет активных кейсов в работе."
    else:
        text = (
            f"📌 <b>Мои кейсы в работе ({total}):</b>\n"
            f"• 📢 Жалобы: {len(my_reports)}\n"
            f"• 🖼️ Фото-кейсы: {len(my_cases_list)}\n"
            f"• 🛡 Верификации: {len(my_verifications)}\n"
            f"• ⚖️ Апелляции: {len(my_appeals)}\n\n"
            f"Выберите кейс для перехода к решению:"
        )

    await _safe_edit_message_text(callback.message, text, reply_markup=my_cases_keyboard(items))
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("mycase:"))
async def mycase_open(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    parts = (callback.data or "").split(":")
    if len(parts) != 3:
        await callback.answer("Некорректный кейс", show_alert=True)
        return
    _, item_type, raw_id = parts
    try:
        item_id = uuid.UUID(raw_id)
    except ValueError:
        await callback.answer("Некорректный идентификатор", show_alert=True)
        return

    try:
        await callback.message.delete()
    except Exception:
        pass

    if item_type == "report":
        report = await ReportRepository(session).get(item_id)
        if not report:
            await callback.message.answer("Жалоба не найдена.", reply_markup=admin_nav_keyboard())
            await _safe_callback_answer(callback, "Жалоба уже удалена.", show_alert=True)
            return
        await _render_report(callback, session, report)
    elif item_type == "case":
        case = await TrustRepository(session).case(item_id)
        if not case:
            await callback.message.answer("Кейс не найден.", reply_markup=admin_nav_keyboard())
            await _safe_callback_answer(callback, "Кейс уже удалён.", show_alert=True)
            return
        await _render_photo_case(callback, session, case)
    elif item_type == "verify":
        req = await TrustRepository(session).verification(item_id)
        if not req:
            await callback.message.answer("Верификация не найдена.", reply_markup=admin_nav_keyboard())
            await _safe_callback_answer(callback, "Верификация уже удалена.", show_alert=True)
            return
        await _render_verification(callback, session, req)
    elif item_type == "appeal":
        appeal = await AppealRepository(session).get(item_id)
        if not appeal:
            await callback.message.answer("Апелляция не найдена.", reply_markup=admin_nav_keyboard())
            await _safe_callback_answer(callback, "Апелляция уже удалена.", show_alert=True)
            return
        await _render_appeal(callback, session, appeal)
    await _safe_callback_answer(callback)


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
    await message.answer("\n".join(lines), parse_mode="HTML")


@router.callback_query(F.data == "admin:reports")
async def reports(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    await _show_next_report(callback, session)
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:browse")
async def admin_browse(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_view_all_profiles):
        return
    target = await _next_browse_user(session)
    if target is None:
        await callback.message.answer(
            "👥 Анкеты отсутствуют.",
            reply_markup=admin_nav_keyboard(refresh_callback="admin:browse", back_callback="admin:section:users"),
        )
        await _safe_callback_answer(callback)
        return
    role = await _role_for_admin(session, callback.from_user.id, settings)
    await _render_admin_browse_profile(callback, session, target.id, role)
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("admin:browse:next"))
async def admin_browse_next(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_view_all_profiles):
        return
    parts = (callback.data or "").split(":")
    current_user_id = None
    if len(parts) >= 4 and parts[1] == "browse" and parts[2] == "next":
        try:
            current_user_id = int(parts[3])
        except ValueError:
            current_user_id = None
    target = await _next_browse_user(session, current_user_id)
    if target is None:
        await callback.message.answer(
            "👥 Анкеты отсутствуют.",
            reply_markup=admin_nav_keyboard(refresh_callback="admin:browse", back_callback="admin:section:users"),
        )
        await _safe_callback_answer(callback)
        return
    role = await _role_for_admin(session, callback.from_user.id, settings)
    await _render_admin_browse_profile(callback, session, target.id, role)
    await _safe_callback_answer(callback, "Следующая анкета")


@router.callback_query(F.data.startswith("profilemod:"))
async def profile_moderation_action(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    parts = (callback.data or "").split(":")
    if len(parts) == 4 and parts[1] == "prompt":
        _, _, action, raw_user_id = parts
        action_names = {
            "ban": "заблокировать",
            "freeze": "заморозить",
            "unban": "разблокировать",
            "unfreeze": "разморозить",
        }
        action_name = action_names.get(action)
        if action_name is None:
            await callback.answer("Некорректное действие", show_alert=True)
            return
        await _safe_edit_message_text(
            callback.message,
            f"⚠️ <b>Подтверждение действия</b>\nВы действительно хотите {action_name} пользователя?",
            reply_markup=confirm_action_keyboard(
                f"profilemod:execute:{action}:{raw_user_id}", back_data="admin:browse"
            ),
        )
        await _safe_callback_answer(callback)
        return
    if len(parts) != 4 or parts[1] != "execute":
        await callback.answer("Некорректное действие", show_alert=True)
        return
    _, _, action, raw_user_id = parts
    try:
        user_id = int(raw_user_id)
    except ValueError:
        await callback.answer("Некорректный пользователь", show_alert=True)
        return
    actor_role = await _role_for_admin(session, callback.from_user.id, settings)
    service = ModerationService(session)
    if user_id == callback.from_user.id:
        await callback.answer("Нельзя применить санкцию к самому себе.", show_alert=True)
        return
    if action == "ban":
        changed = await service.ban(user_id, callback.from_user.id, reason="manual moderation", actor_role=actor_role)
        result = "Пользователь заблокирован."
    elif action == "freeze":
        changed = await service.suspend(
            user_id,
            callback.from_user.id,
            reason="manual moderation",
            actor_role=actor_role,
        )
        result = "Анкета заморожена."
    elif action == "unban":
        if not can_unban(actor_role):
            await callback.answer("Недостаточно прав для разблокировки.", show_alert=True)
            return
        changed = await service.unban(user_id, callback.from_user.id, actor_role=actor_role)
        result = "Пользователь разблокирован."
    elif action == "unfreeze":
        if not can_unfreeze(actor_role):
            await callback.answer("Недостаточно прав для разморозки.", show_alert=True)
            return
        target_user = await session.get(User, user_id)
        if target_user is None or target_user.status != UserStatus.SUSPENDED:
            await callback.answer("Пользователь не находится в заморозке.", show_alert=True)
            return
        target_user.status = UserStatus.ACTIVE
        target_profile = await ProfileRepository(session).by_user_id(user_id)
        if target_profile:
            target_profile.is_visible = True
            target_profile.moderation_locked = False
            target_profile.moderation_status = ModerationStatus.CLEAR
        await TrustRepository(session).log(
            callback.from_user.id,
            "UNFREEZE",
            target_type="user",
            target_id=str(user_id),
            target_user_id=user_id,
            details="manual unfreeze",
        )
        await session.flush()
        changed = True
        result = "Анкета разморожена."
    else:
        await callback.answer("Некорректное действие", show_alert=True)
        return
    if not changed:
        await callback.answer("Действие недоступно для этого пользователя.", show_alert=True)
        return
    await InternalNotificationService(callback.bot, settings).send_moderation_event(
        "Ручная санкция модератора",
        user_id=user_id,
        details=f"Action: {action}; moderator: {callback.from_user.id}",
        event_key=f"profile-{action}:{user_id}",
        target_callback="admin:browse",
    )
    await _safe_edit_message_text(
        callback.message,
        f"✅ {result}",
        reply_markup=admin_nav_keyboard(refresh_callback="admin:browse", back_callback="admin:section:users"),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:verifications")
async def verification_queue(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    await _show_next_verification(callback, session)
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("verify:"))
async def verification_decision(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    try:
        _, action, raw_id = callback.data.split(":")
        if action == "claim":
            request_id = uuid.UUID(raw_id)
            request = await VerificationService(session).claim(request_id, callback.from_user.id)
            if request is None:
                await callback.answer("Заявка уже взята или обработана.", show_alert=True)
                return
            await callback.message.edit_reply_markup(reply_markup=verification_decision_keyboard(str(request.id)))
            await callback.answer("Заявка закреплена за вами.")
            return
        decision = {
            "approve": VerificationDecision.APPROVED,
            "reject": VerificationDecision.REJECTED,
            "retake": VerificationDecision.RETAKE_REQUESTED,
        }.get(action)
        if decision is None and action != "release":
            raise KeyError(action)
        request_id = uuid.UUID(raw_id)
    except (KeyError, ValueError):
        await callback.answer("Некорректное решение", show_alert=True)
        return
    actor_role = await _role_for_admin(session, callback.from_user.id, settings)
    if action == "release":
        request, changed = await VerificationService(session).release(
            request_id, callback.from_user.id, actor_role=actor_role
        )
        if not changed:
            await callback.answer("Заявка уже освобождена или недоступна.", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id,
            "VERIFICATION_RELEASED",
            target_type="verification",
            target_id=str(request.id),
            target_user_id=request.user_id,
        )
        await _safe_edit_message_text(
            callback.message,
            "✅ Верификация освобождена и возвращена в общую очередь.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:verifications", back_callback="admin:section:moderation"
            ),
        )
        await _safe_callback_answer(callback)
        return
    request, changed = await VerificationService(session).decide(
        request_id,
        callback.from_user.id,
        decision,
        actor_role=actor_role,
    )
    if not changed:
        handled_by = await _admin_label(session, request.admin_id if request else None)
        await callback.answer(f"Эта верификация уже обработана модератором {handled_by}.", show_alert=True)
        return
    messages = {
        VerificationDecision.APPROVED: "🟢 Верификация подтверждена.",
        VerificationDecision.REJECTED: "❌ Верификация отклонена.",
        VerificationDecision.RETAKE_REQUESTED: "🔁 Пожалуйста, запишите кружок ещё раз.",
    }
    await NotificationService(callback.bot).safe_send(request.user_id, messages[decision])
    await _safe_edit_message_text(
        callback.message,
        f"✅ Решение сохранено: {decision.value}",
        reply_markup=admin_nav_keyboard(
            refresh_callback="admin:verifications", back_callback="admin:section:moderation"
        ),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:nsfw")
async def nsfw_queue(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    await _show_next_photo_case(callback, session)
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:blocked")
async def blocked_users(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    users = list((await session.scalars(select(User).where(User.status == UserStatus.BANNED).limit(30))).all())
    if not users:
        await _safe_edit_message_text(
            callback.message,
            "🚫 <b>Заблокированные пользователи</b>\n\nЗаблокированных пользователей нет.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:blocked", back_callback="admin:section:users"
            ),
        )
    else:
        names = []
        for user in users:
            label = user_display_name(user.id, username=user.username)
            names.append(f"• {label} (ID: <code>{user.id}</code>)")
        text = (
            f"🚫 <b>Заблокированные пользователи ({len(users)}):</b>\n\n"
            + "\n".join(names)
            + "\n\n<i>Для управления статусом перейдите в «Просмотр анкет».</i>"
        )
        await _safe_edit_message_text(
            callback.message,
            text,
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:blocked", back_callback="admin:section:users"
            ),
        )
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("case:"))
async def moderation_case(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    try:
        _, action, raw_id = callback.data.split(":")
        case_id = uuid.UUID(raw_id)
    except ValueError:
        await callback.answer("Некорректный кейс", show_alert=True)
        return
    service = ModerationService(session)
    actor_role = await _role_for_admin(session, callback.from_user.id, settings)
    if action == "claim":
        case, changed, reason = await service.claim_case(case_id, callback.from_user.id, actor_role=actor_role)
        if not changed:
            if reason == "already_assigned":
                handled_by = await _admin_label(session, case.assigned_to if case else None)
                await callback.answer(f"Кейс уже взял {handled_by}.", show_alert=True)
            else:
                await callback.answer("Кейс уже нельзя взять в работу.", show_alert=True)
            return
        await InternalNotificationService(callback.bot, settings).send_moderation_event(
            "Кейс взят в работу",
            user_id=case.user_id,
            case_id=str(case.id),
            details=f"Moderator: {callback.from_user.id}",
            event_key=f"case-claimed:{case.id}",
            target_callback=f"mycase:case:{case.id}",
        )
        await callback.message.edit_reply_markup(reply_markup=case_decision_keyboard(str(case.id)))
        await callback.answer("Кейс закреплён за вами.")
        return
    if action == "release":
        case, changed, reason = await service.release_case(
            case_id, callback.from_user.id, moderator_id=callback.from_user.id
        )
        if not changed:
            await callback.answer(reason or "Кейс уже освобождён или недоступен.", show_alert=True)
            return
        await _safe_edit_message_text(
            callback.message,
            "✅ Кейс освобождён и возвращён в общую очередь.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:nsfw", back_callback="admin:section:moderation"
            ),
        )
        await _safe_callback_answer(callback)
        return
    if action not in {"restore", "retake", "reject"}:
        await callback.answer("Некорректное решение по кейсу.", show_alert=True)
        return
    case, changed, _ = await service.resolve_case(
        case_id,
        callback.from_user.id,
        restore=action == "restore",
        retake=action == "retake",
        reject=action == "reject",
        actor_role=actor_role,
    )
    if not changed:
        handled_by = await _admin_label(session, case.admin_id if case else None)
        await callback.answer(f"Этот кейс уже обработан модератором {handled_by}.", show_alert=True)
        return
    if action == "restore":
        user_message = "✅ Фото одобрено. Ваша анкета снова видна в знакомствах."
        result = "✅ Фото одобрено, анкета восстановлена."
    elif action == "reject":
        user_message = (
            "❌ Фото отклонено. Анкета скрыта; откройте «Моя анкета» → «Управлять фото» "
            "и загрузите новое фото."
        )
        result = "❌ Фото отклонено, анкета скрыта; пользователю предложена замена фото."
    else:
        user_message = (
            "📝 Фото нужно заменить. Откройте «Моя анкета» → «Управлять фото» "
            "и загрузите новое фото. Анкета останется скрытой до отдельного "
            "решения модератора."
        )
        result = "📝 Пользователю отправлен запрос на замену фотографии; ограничение сохранено."
    await NotificationService(callback.bot).safe_send(case.user_id, user_message)
    await InternalNotificationService(callback.bot, settings).send_moderation_event(
        "Кейс решён",
        user_id=case.user_id,
        case_id=str(case.id),
        details=f"Decision: {action}; moderator: {callback.from_user.id}",
        event_key=f"case-resolved:{case.id}",
    )
    await _safe_edit_message_text(
        callback.message,
        result,
        reply_markup=admin_nav_keyboard(refresh_callback="admin:nsfw", back_callback="admin:section:moderation"),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:trust_history")
async def trust_history(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_view_audit_history):
        return
    items = await TrustRepository(session).history()
    lines = ["📜 <b>История решений модерации:</b>\n"] + [
        f"• {item.created_at:%d.%m %H:%M}: <code>{item.action}</code> → {item.target_id or '—'}" for item in items
    ]
    text = "\n".join(lines[:31]) if items else "История решений пуста."
    await _safe_edit_message_text(
        callback.message,
        text,
        reply_markup=admin_nav_keyboard(
            refresh_callback="admin:trust_history", back_callback="admin:section:stats"
        ),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:trust_stats")
async def trust_stats(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    stats = await TrustStatsService(session).snapshot()
    text = (
        "📊 <b>Общая статистика Trust</b>\n\n"
        f"• Проверенных пользователей: <b>{stats['verified']}</b>\n"
        f"• Всего жалоб: <b>{stats['reports']}</b>\n"
        f"• Ложных жалоб: <b>{stats['false_reports']}</b>\n"
        f"• Подтверждённых нарушений: <b>{stats['confirmed_fakes']}</b>\n"
        f"• Средний Trust Score: <b>{stats['average_trust_score']}</b>"
    )
    await _safe_edit_message_text(
        callback.message,
        text,
        reply_markup=admin_nav_keyboard(
            refresh_callback="admin:trust_stats", back_callback="admin:section:stats"
        ),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("moderate:"))
async def moderate(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    parts = (callback.data or "").split(":")
    if not parts or parts[0] != "moderate":
        return
    if len(parts) == 4 and parts[1] == "prompt":
        _, _, action, raw_id = parts
        action_text = {
            "ban": "заблокировать пользователя",
            "hide": "скрыть анкету",
            "dismiss": "отклонить жалобу",
        }.get(action)
        if action_text is None:
            await callback.answer("Некорректное действие", show_alert=True)
            return
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
        if report.assigned_to != callback.from_user.id:
            await callback.answer("Сначала возьмите жалобу в работу.", show_alert=True)
            return
        confirm_data = f"moderate:execute:{action}:{raw_id}"
        await _safe_edit_message_text(
            callback.message,
            f"⚠️ <b>Подтвердите действие:</b> {action_text}.\n\nПосле подтверждения это действие нельзя будет отменить.",
            reply_markup=confirm_action_keyboard(confirm_data, back_data="admin:reports"),
        )
        await _safe_callback_answer(callback)
        return
    if len(parts) == 3 and parts[1] == "claim":
        _, _, raw_id = parts
        try:
            report_id = uuid.UUID(raw_id)
        except ValueError:
            await callback.answer("Некорректная жалоба", show_alert=True)
            return
        report = await ReportRepository(session).claim(report_id, callback.from_user.id)
        if report is None:
            await callback.answer("Жалоба уже взята или обработана.", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id,
            "REPORT_CLAIMED",
            target_type="report",
            target_id=str(report.id),
            target_user_id=report.target_user_id,
        )
        await callback.message.edit_reply_markup(reply_markup=moderation_decision_keyboard(str(report.id)))
        await callback.answer("Жалоба закреплена за вами.")
        return
    if len(parts) == 3 and parts[1] == "release":
        _, _, raw_id = parts
        try:
            report_id = uuid.UUID(raw_id)
        except ValueError:
            await callback.answer("Некорректная жалоба", show_alert=True)
            return
        role = await _role_for_admin(session, callback.from_user.id, settings)
        released = await ReportRepository(session).release(
            report_id, callback.from_user.id, override=can_override_case(role)
        )
        if released is None:
            await callback.answer("Жалоба уже освобождена или недоступна.", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id,
            "REPORT_RELEASED",
            target_type="report",
            target_id=str(released.id),
            target_user_id=released.target_user_id,
        )
        await _safe_edit_message_text(
            callback.message,
            "✅ Жалоба освобождена и возвращена в общую очередь.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:reports", back_callback="admin:section:moderation"
            ),
        )
        await _safe_callback_answer(callback)
        return
    if len(parts) == 4 and parts[1] == "execute":
        _, _, action, raw_id = parts
    elif len(parts) == 3:
        _, action, raw_id = parts
    else:
        await callback.answer("Некорректная жалоба", show_alert=True)
        return
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
    if report.assigned_to != callback.from_user.id:
        await callback.answer("Сначала возьмите жалобу в работу.", show_alert=True)
        return
    if action == "ban":
        try:
            async with session.begin_nested():
                resolved = await ReportService(session, threshold=settings.report_threshold).confirm_fake(
                    report_id, callback.from_user.id
                )
                if resolved is None:
                    raise _SanctionNotApplied
                banned = await ModerationService(session).ban(
                    report.target_user_id,
                    callback.from_user.id,
                    reason="report",
                    actor_role=await _role_for_admin(session, callback.from_user.id, settings),
                )
                if not banned:
                    raise _SanctionNotApplied
        except _SanctionNotApplied:
            await callback.answer("Не удалось применить блокировку", show_alert=True)
            return
        result = "Пользователь заблокирован."
    elif action == "hide":
        try:
            async with session.begin_nested():
                resolved = await repo.resolve(report_id, ReportStatus.APPROVED)
                if resolved is None:
                    raise _SanctionNotApplied
                suspended = await ModerationService(session).suspend(
                    report.target_user_id,
                    callback.from_user.id,
                    reason="report",
                    actor_role=await _role_for_admin(session, callback.from_user.id, settings),
                )
                if not suspended:
                    raise _SanctionNotApplied
        except _SanctionNotApplied:
            await callback.answer("Не удалось применить ограничение", show_alert=True)
            return
        await NotificationService(callback.bot).safe_send(
            report.target_user_id,
            "⏸ Ваша анкета временно приостановлена модерацией. Вы можете нажать «🆘 Апелляция» и описать ситуацию.",
        )
        result = "Анкета приостановлена и скрыта. Пользователю предложена апелляция."
    elif action == "dismiss":
        resolved = await ReportService(session, threshold=settings.report_threshold).dismiss(
            report_id, callback.from_user.id
        )
        if resolved is None:
            await callback.answer("Жалоба уже обработана", show_alert=True)
            return
        result = "Жалоба отклонена."
    else:
        await callback.answer("Некорректное действие", show_alert=True)
        return
    await InternalNotificationService(callback.bot, settings).send_moderation_event(
        "Решение по жалобе",
        user_id=report.target_user_id,
        case_id=str(report.id),
        details=f"Decision: {action}; moderator: {callback.from_user.id}",
        event_key=f"report-decision:{report.id}",
        target_callback=f"mycase:report:{report.id}",
    )
    await _safe_edit_message_text(
        callback.message,
        f"✅ {result}",
        reply_markup=admin_nav_keyboard(refresh_callback="admin:reports", back_callback="admin:section:moderation"),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:appeals")
async def appeals(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    await _show_next_appeal(callback, session, callback.from_user.id)
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("appeal:"))
async def appeal_action(callback: CallbackQuery, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    parts = (callback.data or "").split(":")
    if len(parts) == 3 and parts[1] == "claim":
        try:
            appeal_id = uuid.UUID(parts[2])
        except ValueError:
            await callback.answer("Некорректная апелляция", show_alert=True)
            return
        appeal = await AppealRepository(session).claim(appeal_id, callback.from_user.id)
        if appeal is None:
            await callback.answer("Апелляция уже взята или обработана.", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id,
            "APPEAL_CLAIMED",
            target_type="appeal",
            target_id=str(appeal.id),
            target_user_id=appeal.user_id,
        )
        await callback.message.edit_reply_markup(reply_markup=appeal_decision_keyboard(str(appeal.id)))
        await callback.answer("Апелляция закреплена за вами.")
        return
    if len(parts) == 4 and parts[1] == "prompt":
        _, _, action, raw_id = parts
        if action not in {"restore", "reject"}:
            await callback.answer("Некорректное решение по апелляции", show_alert=True)
            return
        action_name = "отклонение апелляции" if action == "reject" else "одобрение апелляции"
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
        if appeal.assigned_to != callback.from_user.id:
            await callback.answer("Сначала возьмите апелляцию в работу.", show_alert=True)
            return
        await _safe_edit_message_text(
            callback.message,
            f"⚠️ <b>Подтвердите {action_name}.</b>\n\nПосле подтверждения решение нельзя будет отменить.",
            reply_markup=confirm_action_keyboard(f"appeal:execute:{action}:{raw_id}", back_data="admin:appeals"),
        )
        await _safe_callback_answer(callback)
        return
    if len(parts) == 4 and parts[1] == "execute":
        _, _, action, raw_id = parts
    elif len(parts) == 3 and parts[1] in {"release", "reply", "restore", "reject"}:
        try:
            _, action, raw_id = parts
        except (ValueError, TypeError):
            await callback.answer("Некорректная апелляция", show_alert=True)
            return
    else:
        await callback.answer("Некорректная апелляция", show_alert=True)
        return
    try:
        appeal_id = uuid.UUID(raw_id)
    except (ValueError, TypeError):
        await callback.answer("Некорректная апелляция", show_alert=True)
        return
    repo = AppealRepository(session)
    appeal = await repo.get(appeal_id)
    if appeal is None or appeal.status != AppealStatus.PENDING:
        await callback.answer("Апелляция уже обработана", show_alert=True)
        return
    actor_role = await _role_for_admin(session, callback.from_user.id, settings)
    override = can_override_appeal_assignment(actor_role)
    if action == "release":
        released = await repo.release(appeal_id, callback.from_user.id, override=override)
        if released is None:
            await callback.answer("Апелляция уже освобождена или недоступна.", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id,
            "APPEAL_RELEASED",
            target_type="appeal",
            target_id=str(released.id),
            target_user_id=released.user_id,
        )
        await _safe_edit_message_text(
            callback.message,
            "✅ Апелляция освобождена и возвращена в общую очередь.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:appeals", back_callback="admin:section:moderation"
            ),
        )
        await _safe_callback_answer(callback)
        return
    if appeal.assigned_to != callback.from_user.id and not override:
        await callback.answer("Сначала возьмите апелляцию в работу.", show_alert=True)
        return
    if action == "reply":
        user = await UserRepository(session).get(appeal.user_id)
        username = user.username if user else None
        contact = f"@{username}" if username else f"ID: {appeal.user_id}"
        template = (
            "Здравствуйте. Я модератор MeAnima. Пишу вам по поводу вашей "
            "апелляции на ограничение анкеты. Расскажите, пожалуйста, что "
            "произошло..."
        )
        await callback.message.answer(
            "💬 <b>Связь с пользователем:</b>\n"
            "Напишите пользователю со своего личного Telegram-аккаунта.\n\n"
            f"👤 Контакт: <b>{contact}</b>\n"
            f'📝 Шаблон сообщения: "<i>{template}</i>"\n\n'
            "<i>Бот не отправляет это сообщение и не является посредником переписки.</i>",
            parse_mode="HTML",
            reply_markup=admin_nav_keyboard(refresh_callback="admin:appeals", back_callback="admin:appeals"),
        )
        await _safe_callback_answer(callback)
        return
    if action in {"restore", "approve"}:
        restored, restore_reason = await ModerationService(session).restore_appeal_sanction(
            appeal, callback.from_user.id, actor_role=actor_role
        )
        if not restored:
            message = (
                "Недостаточно прав для снятия ограничения."
                if restore_reason == "forbidden"
                else "Нельзя снять это ограничение: есть другая открытая санкция."
                if restore_reason == "other_open_sanction"
                else "Ограничение уже не может быть снято."
            )
            await callback.answer(message, show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id, "appeal_restored", target_type="appeal", target_id=str(appeal_id)
        )
        await NotificationService(callback.bot).safe_send(
            appeal.user_id,
            "✅ Апелляция одобрена. Ограничение снято; при желании включите видимость анкеты.",
        )
        result = "Апелляция одобрена, аккаунт восстановлен."
    elif action == "reject":
        resolved = await repo.resolve(appeal_id, AppealStatus.REJECTED, callback.from_user.id)
        if resolved is None:
            await callback.answer("Апелляция уже обработана", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id, "appeal_rejected", target_type="appeal", target_id=str(appeal_id)
        )
        await NotificationService(callback.bot).safe_send(
            appeal.user_id, "❌ Апелляция отклонена. Анкета остаётся приостановленной."
        )
        result = "Апелляция отклонена."
    else:
        await callback.answer("Некорректная апелляция", show_alert=True)
        return
    await InternalNotificationService(callback.bot, settings).send_moderation_event(
        "Решение по апелляции",
        user_id=appeal.user_id,
        case_id=str(appeal.id),
        details=f"Decision: {action}; moderator: {callback.from_user.id}",
        event_key=f"appeal-decision:{appeal.id}",
        target_callback=f"mycase:appeal:{appeal.id}",
    )
    await _safe_edit_message_text(
        callback.message,
        f"✅ {result}",
        reply_markup=admin_nav_keyboard(refresh_callback="admin:appeals", back_callback="admin:section:moderation"),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:broadcast")
async def broadcast_start(callback: CallbackQuery, state: FSMContext, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    await state.set_state(AdminState.broadcast_message)
    await _safe_edit_message_text(
        callback.message,
        "📣 <b>Рассылка сообщений</b>\n\nОтправьте текст рассылки. Его получат все активные пользователи.",
        reply_markup=admin_nav_keyboard(back_callback="admin:section:administration"),
    )
    await _safe_callback_answer(callback)


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
    await message.answer(
        f"✅ <b>Рассылка завершена.</b>\nДоставлено пользователям: <b>{delivered}</b>.",
        reply_markup=admin_nav_keyboard(back_callback="admin:section:administration"),
        parse_mode="HTML",
    )
