from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.verification import verification_start
from keyboards.dating import dating_keyboard, report_reasons_keyboard
from models import ReportReason, User, UserStatus
from repositories.discovery import DiscoveryRepository
from repositories.profile import ProfileRepository
from repositories.trust import TrustRepository
from services.interest_normalizer import format_interests
from services.like_service import LikeService
from services.match_service import MatchService
from services.notification_service import InternalNotificationService, NotificationService
from services.profile_service import ProfileService
from services.promo_service import get_empty_discovery_promo
from services.recommendation import RecommendationService
from services.report_service import ReportService
from states.dating import DatingState
from utils.admin_ui import user_display_name
from utils.contacts import telegram_contact
from utils.document_links import documents_keyboard
from utils.profile_media import profile_photo_ids, send_profile_gallery
from utils.text import escape_html

router = Router()


def _target_id(callback: CallbackQuery) -> int | None:
    try:
        return int((callback.data or "").split(":")[1])
    except (IndexError, TypeError, ValueError):
        return None


async def _clear_callback_keyboard(callback: CallbackQuery) -> None:
    """Deactivate a consumed discovery card so its action cannot be repeated."""
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest as exc:
        if "message is not modified" not in str(exc).lower():
            raise


async def show_next(message: Message, user_id: int, session: AsyncSession, settings) -> None:
    profile = await ProfileService(session).get_profile(user_id)
    if profile is None:
        await message.answer(
            "📝 Для начала нужно создать анкету.\n\nБез неё мы не сможем подобрать подходящих людей.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="✨ Создать анкету", callback_data="profile:create")]]
            ),
        )
        return
    user = await session.get(User, user_id)
    if user is None or user.status != UserStatus.ACTIVE:
        await message.answer(
            "⏸️ Ваш аккаунт временно ограничен. Доступ к знакомствам будет восстановлен после решения модератора."
        )
        return
    if profile.moderation_locked or profile.moderation_status.value == "UNDER_REVIEW":
        await message.answer(
            "⏳ Ваша анкета сейчас на проверке или ожидает замены фотографии. Пока она не участвует в знакомствах.\n\n"
            "Откройте анкету, чтобы увидеть статус и заменить фото или подать апелляцию.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="📷 Управлять фото", callback_data="profile:photos")]]
            ),
        )
        return
    recommendation = await RecommendationService(session, weights=settings.matching_weights).next_recommendation(
        user_id
    )
    if not recommendation:
        promo = get_empty_discovery_promo(user_id, profile=profile)
        empty_kb_rows = [
            [
                InlineKeyboardButton(text="🔄 Обновить выдачу", callback_data="next:profile"),
                InlineKeyboardButton(text="👤 Моя анкета", callback_data="promo:my_profile"),
            ]
        ]
        if promo["button_action"] == "promo:share":
            bot_info = await message.bot.get_me()
            bot_username = bot_info.username
            share_text = "Присоединяйся к MeAnima для знакомств!"
            share_url = f"https://t.me/share/url?url=https://t.me/{bot_username}&text={share_text}"
            empty_kb_rows.append([InlineKeyboardButton(text=promo["button_text"], url=share_url)])
        elif promo["button_action"] not in {"next:profile", "promo:my_profile"}:
            action_btn = InlineKeyboardButton(text=promo["button_text"], callback_data=promo["button_action"])
            empty_kb_rows.append([action_btn])

        empty_kb = InlineKeyboardMarkup(inline_keyboard=empty_kb_rows)
        await message.answer(
            "✨ Похоже, ты посмотрел всех доступных людей поблизости.\n\n"
            f"<b>{escape_html(promo['title'])}</b>\n"
            f"{escape_html(promo['text'])}",
            reply_markup=empty_kb,
        )
        return
    p = recommendation.profile
    caption = (
        f"{escape_html(p.name)}, {p.age}\n📍 {escape_html(p.district)}\n"
        f"🏫 {escape_html(p.institution)}\n🎯 {escape_html(format_interests(p.interests))}\n\n{escape_html(p.bio)}"
    )
    if p.verification_status.value == "VERIFIED":
        caption += "\n\n🟢 Проверенный профиль"
    caption += f"\n\n❤️ Совместимость: {round(recommendation.score)}%"
    await send_profile_gallery(message, p, caption, dating_keyboard(p.user_id))


@router.message(F.text.in_({"💘 Знакомства", "💘 Смотреть анкеты", "Смотреть анкеты"}))
async def browse(message: Message, session: AsyncSession, settings) -> None:
    await show_next(message, message.from_user.id, session, settings)


@router.callback_query(F.data.startswith("like:"))
async def like(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    try:
        result = await LikeService(session).create(callback.from_user.id, target)
    except ValueError as error:
        await callback.answer(str(error), show_alert=True)
        return
    if not result.created:
        await _clear_callback_keyboard(callback)
        await callback.answer("Лайк уже был отправлен.")
        return
    await _clear_callback_keyboard(callback)
    match = await MatchService(session).create_if_mutual(callback.from_user.id, target, result.like)
    await callback.answer("Это взаимно! 🎉" if match.created else "Лайк отправлен ❤️")
    rec_svc = RecommendationService(session, weights=settings.matching_weights)
    await rec_svc.remove_candidate(callback.from_user.id, target)
    notifier = NotificationService(callback.bot)
    if match.created:
        target_profile, target_user = await DiscoveryRepository(session).profile_and_user(target)
        source_contact = telegram_contact(
            callback.from_user.id, callback.from_user.username, callback.from_user.full_name
        )
        target_contact = telegram_contact(
            target,
            target_user.username if target_user else None,
            target_profile.name if target_profile else "Пользователь",
        )
        target_url = f"https://t.me/{target_user.username}" if target_user and target_user.username else f"tg://user?id={target}"
        match_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="💬 Написать", url=target_url),
                    InlineKeyboardButton(text="💘 Продолжить поиск", callback_data="next:profile"),
                ]
            ]
        )
        target_name = escape_html(target_profile.name if target_profile else 'пользователем')
        source_profile, _ = await DiscoveryRepository(session).profile_and_user(callback.from_user.id)
        fallback_source = callback.from_user.full_name or "Пользователь"
        source_name = escape_html(source_profile.name if source_profile else fallback_source)

        match_target_text = (
            f"🎉 <b>У вас взаимная симпатия с {source_name}!</b>\n\n"
            f"Кажется, вы понравились друг другу! ✨ Не стесняйтесь сделать первый шаг и написать прямо сейчас.\n\n"
            f"💬 <b>Контакт для связи:</b> {source_contact}\n\n"
            f"Желаем вам приятного и тёплого общения! 💫"
        )
        match_source_text = (
            f"🎉 <b>У вас взаимная симпатия с {target_name}!</b>\n\n"
            f"Кажется, вы понравились друг другу! ✨ Не стесняйтесь сделать первый шаг и написать прямо сейчас.\n\n"
            f"💬 <b>Контакт для связи:</b> {target_contact}\n\n"
            f"Желаем вам приятного и тёплого общения! 💫"
        )

        source_url = f"https://t.me/{callback.from_user.username}" if callback.from_user.username else f"tg://user?id={callback.from_user.id}"
        await notifier.safe_send(
            target,
            match_target_text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="💬 Написать", url=source_url),
                        InlineKeyboardButton(text="💘 Продолжить поиск", callback_data="next:profile"),
                    ]
                ]
            ),
        )
        await callback.message.answer(
            match_source_text,
            reply_markup=match_kb,
        )
    else:
        await notifier.safe_send(target, "💌 Кому-то понравилась ваша анкета.")
    await show_next(callback.message, callback.from_user.id, session, settings)


@router.callback_query(F.data.startswith("comment:"))
async def comment_start(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    from services.eligibility import EligibilityError, EligibilityService

    try:
        await EligibilityService(session).ensure_recommendation_action_allowed(
            callback.from_user.id, target, action="поставить лайк"
        )
    except EligibilityError as error:
        await callback.answer(str(error), show_alert=True)
        return
    await state.update_data(like_target=target)
    await state.set_state(DatingState.like_comment)
    await callback.message.answer("💌 Напишите короткое сообщение к лайку (до 200 символов).")
    await callback.answer()


@router.message(DatingState.like_comment)
async def comment_finish(message: Message, state: FSMContext, session: AsyncSession, settings) -> None:
    text = (message.text or "").strip()
    if not 1 <= len(text) <= 200:
        await message.answer("⚠️ Сообщение должно быть от 1 до 200 символов.")
        return
    target = (await state.get_data())["like_target"]
    try:
        result = await LikeService(session).create(message.from_user.id, target, text)
    except ValueError as error:
        await state.clear()
        await message.answer(str(error))
        return
    await state.clear()
    if not result.created:
        await message.answer("❤️ Лайк уже был отправлен ранее.")
        return
    match = await MatchService(session).create_if_mutual(message.from_user.id, target, result.like)
    rec_svc = RecommendationService(session, weights=settings.matching_weights)
    await rec_svc.remove_candidate(message.from_user.id, target)
    notifier = NotificationService(message.bot)
    await notifier.safe_send(target, "💌 Кому-то понравилась ваша анкета.\n\n" + escape_html(text))
    if match.created:
        target_profile, target_user = await DiscoveryRepository(session).profile_and_user(target)
        source_profile, _ = await DiscoveryRepository(session).profile_and_user(message.from_user.id)
        source_contact = telegram_contact(message.from_user.id, message.from_user.username, message.from_user.full_name)
        target_contact = telegram_contact(
            target,
            target_user.username if target_user else None,
            target_profile.name if target_profile else "Пользователь",
        )
        target_url = f"https://t.me/{target_user.username}" if target_user and target_user.username else f"tg://user?id={target}"
        source_url = f"https://t.me/{message.from_user.username}" if message.from_user.username else f"tg://user?id={message.from_user.id}"

        target_name = escape_html(target_profile.name if target_profile else 'пользователем')
        fallback_source = message.from_user.full_name or "Пользователь"
        source_name = escape_html(source_profile.name if source_profile else fallback_source)

        match_target_text = (
            f"🎉 <b>У вас взаимная симпатия с {source_name}!</b>\n\n"
            f"Кажется, вы понравились друг другу! ✨ Не стесняйтесь сделать первый шаг и написать прямо сейчас.\n\n"
            f"💬 <b>Контакт для связи:</b> {source_contact}\n\n"
            f"Желаем вам приятного и тёплого общения! 💫"
        )
        match_source_text = (
            f"🎉 <b>У вас взаимная симпатия с {target_name}!</b>\n\n"
            f"Кажется, вы понравились друг другу! ✨ Не стесняйтесь сделать первый шаг и написать прямо сейчас.\n\n"
            f"💬 <b>Контакт для связи:</b> {target_contact}\n\n"
            f"Желаем вам приятного и тёплого общения! 💫"
        )

        match_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="💬 Написать", url=target_url),
                    InlineKeyboardButton(text="💘 Продолжить поиск", callback_data="next:profile"),
                ]
            ]
        )
        await notifier.safe_send(
            target,
            match_target_text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="💬 Написать", url=source_url),
                        InlineKeyboardButton(text="💘 Продолжить поиск", callback_data="next:profile"),
                    ]
                ]
            ),
        )
        await message.answer(match_source_text, reply_markup=match_kb)
    else:
        await message.answer("❤️ Лайк с сообщением отправлен.")


@router.callback_query(F.data == "promo:verification")
async def promo_verification(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await callback.answer()
    await verification_start(callback.message, state, session)


@router.callback_query(F.data == "promo:confession")
async def promo_confession(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await callback.answer()
    from handlers.confessions import begin
    await begin(callback.message, state, session)


@router.callback_query(F.data == "next:profile")
async def next_profile(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    await callback.answer("Ищу следующую анкету...")
    await show_next(callback.message, callback.from_user.id, session, settings)


@router.callback_query(F.data.startswith("skip:"))
async def skip(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    from services.eligibility import EligibilityError, EligibilityService

    try:
        await EligibilityService(session).ensure_recommendation_action_allowed(
            callback.from_user.id, target, action="пропустить анкету"
        )
    except EligibilityError as error:
        await callback.answer(str(error), show_alert=True)
        return
    await DiscoveryRepository(session).skip(callback.from_user.id, target)
    await RecommendationService(session, weights=settings.matching_weights).skip(callback.from_user.id, target)
    await _clear_callback_keyboard(callback)
    await callback.answer("Анкета больше не будет показана. Ищу следующую анкету...")
    await show_next(callback.message, callback.from_user.id, session, settings)


@router.callback_query(F.data.startswith("block:"))
async def block(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    if not await DiscoveryRepository(session).block(callback.from_user.id, target):
        await callback.answer("Анкета уже недоступна.", show_alert=True)
        return
    await _clear_callback_keyboard(callback)
    await callback.answer("Пользователь заблокирован. Ищу следующую анкету...")
    rec_svc = RecommendationService(session, weights=settings.matching_weights)
    await rec_svc.remove_candidate(callback.from_user.id, target)
    await show_next(callback.message, callback.from_user.id, session, settings)


@router.callback_query(F.data.startswith("report:"))
async def report(callback: CallbackQuery, session: AsyncSession) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    await callback.message.answer(
        "⚠️ Жалоба отправляется модераторам.\n\nПроверьте правила сообщества и процесс модерации:",
        reply_markup=documents_keyboard("community", "safety", "moderation"),
    )
    await callback.message.answer("📌 Выберите причину жалобы:", reply_markup=report_reasons_keyboard(target))
    await callback.answer()


@router.callback_query(F.data.startswith("report_reason:"))
async def report_reason(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    try:
        _, raw_target, reason = (callback.data or "").split(":")
        target = int(raw_target)
        report_reason_value = ReportReason(reason)
    except (ValueError, TypeError):
        await callback.answer("Некорректная жалоба.", show_alert=True)
        return
    try:
        report, created, threshold_reached = await ReportService(session, threshold=settings.report_threshold).submit(
            callback.from_user.id, target, report_reason_value
        )
    except ValueError as error:
        await callback.answer(str(error), show_alert=True)
        return
    rec_svc = RecommendationService(session, weights=settings.matching_weights)
    await rec_svc.remove_candidate(callback.from_user.id, target)
    profile = await ProfileRepository(session).by_user_id(target)
    internal = InternalNotificationService(callback.bot, settings)
    await internal.send_moderation_event(
        "Новая жалоба",
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        reason=report_reason_value.value,
        case_id=str(report.id),
        target_callback=f"mycase:report:{report.id}",
        details=f"Target user: {user_display_name(target)} | created={created}",
        photo_file_ids=profile_photo_ids(profile),
    )
    if threshold_reached:
        for admin_id in settings.admin_ids:
            await NotificationService(callback.bot).safe_send(
                admin_id,
                f"⚠️ Анкета {user_display_name(target)} автоматически снята с публикации: достигнут порог жалоб.",
                dedupe_key=f"report-threshold:{target}",
            )
            await TrustRepository(session).log(
                admin_id,
                "report_threshold_notice_sent",
                target_type="report",
                target_id=str(target),
                metadata={"target_user_id": target},
            )
        await internal.send_moderation_event(
            "⚠️ Profile frozen",
            user_id=target,
            username=None,
            reason=f"3 reports ({settings.report_threshold})",
            case_id=str(report.id),
            target_callback=f"mycase:report:{report.id}",
            details="Автоматическая заморозка анкеты после достижения порога жалоб.",
            photo_file_ids=profile_photo_ids(profile),
        )
    await callback.message.edit_text("✅ Жалоба отправлена модераторам." if created else "Эта жалоба уже была учтена.")
    await callback.answer("Спасибо за помощь")
