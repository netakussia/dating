from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.dating import dating_keyboard, report_reasons_keyboard
from models import ReportReason
from repositories.discovery import DiscoveryRepository
from repositories.report import ReportRepository
from services.like_service import LikeService
from services.match_service import MatchService
from services.notification_service import NotificationService
from services.recommendation import RecommendationService
from states.dating import DatingState
from utils.contacts import telegram_contact

router = Router()


def _target_id(callback: CallbackQuery) -> int | None:
    try:
        return int((callback.data or "").split(":")[1])
    except (IndexError, TypeError, ValueError):
        return None


async def show_next(message: Message, user_id: int, session: AsyncSession, settings) -> None:
    recommendation = await RecommendationService(
        session, weights=settings.matching_weights
    ).next_recommendation(user_id)
    if not recommendation:
        await message.answer("Сейчас подходящих анкет нет. Загляните позже.")
        return
    p = recommendation.profile
    caption = f"{p.name}, {p.age}\n📍 {p.district}\n🏫 {p.institution}\n🎯 {', '.join(p.interests)}\n\n{p.bio}"
    caption += f"\n\n❤️ Совместимость: {round(recommendation.score)}%"
    await message.answer_photo(p.photo_file_id, caption=caption, reply_markup=dating_keyboard(p.user_id))


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
        await callback.answer("Лайк уже был отправлен.")
        return
    match = await MatchService(session).create_if_mutual(callback.from_user.id, target, result.like)
    await callback.answer("Это взаимно! 🎉" if match.created else "Лайк отправлен ❤️")
    RecommendationService(session, weights=settings.matching_weights).remove_candidate(callback.from_user.id, target)
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
        await notifier.safe_send(target, f"🎉 У вас взаимная симпатия!\nКонтакт: {source_contact}")
        await callback.message.answer(f"🎉 У вас взаимная симпатия!\nКонтакт: {target_contact}")
    else:
        await notifier.safe_send(target, "💌 Кому-то понравилась ваша анкета.")
    await show_next(callback.message, callback.from_user.id, session, settings)

@router.callback_query(F.data.startswith("comment:"))
async def comment_start(callback: CallbackQuery, state: FSMContext) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    await state.update_data(like_target=target)
    await state.set_state(DatingState.like_comment)
    await callback.message.answer("Напишите короткое сообщение к лайку (до 200 символов).")
    await callback.answer()

@router.message(DatingState.like_comment)
async def comment_finish(message: Message, state: FSMContext, session: AsyncSession, settings) -> None:
    text = (message.text or "").strip()
    if not 1 <= len(text) <= 200:
        await message.answer("Сообщение должно быть от 1 до 200 символов.")
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
        await message.answer("Лайк уже был отправлен ранее.")
        return
    match = await MatchService(session).create_if_mutual(message.from_user.id, target, result.like)
    RecommendationService(session, weights=settings.matching_weights).remove_candidate(message.from_user.id, target)
    notifier = NotificationService(message.bot)
    await notifier.safe_send(target, "💌 Кому-то понравилась ваша анкета.\n\n" + text)
    if match.created:
        target_profile, target_user = await DiscoveryRepository(session).profile_and_user(target)
        source_contact = telegram_contact(message.from_user.id, message.from_user.username, message.from_user.full_name)
        target_contact = telegram_contact(
            target,
            target_user.username if target_user else None,
            target_profile.name if target_profile else "Пользователь",
        )
        await notifier.safe_send(target, f"🎉 У вас взаимная симпатия!\nКонтакт: {source_contact}")
        await message.answer(f"🎉 У вас взаимная симпатия!\nКонтакт: {target_contact}")
    else:
        await message.answer("❤️ Лайк с сообщением отправлен.")
@router.callback_query(F.data.startswith("skip:"))
async def skip(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    await DiscoveryRepository(session).skip(callback.from_user.id, target)
    await RecommendationService(session, weights=settings.matching_weights).skip(callback.from_user.id, target)
    await callback.answer("Анкета больше не будет показана")
    await show_next(callback.message, callback.from_user.id, session, settings)

@router.callback_query(F.data.startswith("block:"))
async def block(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    await DiscoveryRepository(session).block(callback.from_user.id, target)
    await callback.answer("Пользователь заблокирован")
    RecommendationService(session, weights=settings.matching_weights).remove_candidate(callback.from_user.id, target)
    await show_next(callback.message, callback.from_user.id, session, settings)

@router.callback_query(F.data.startswith("report:"))
async def report(callback: CallbackQuery, session: AsyncSession) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    await callback.message.answer("Выберите причину жалобы:", reply_markup=report_reasons_keyboard(target))
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
    _, created, threshold_reached = await ReportRepository(session).add(
        callback.from_user.id, target, report_reason_value, threshold=settings.report_threshold
    )
    await DiscoveryRepository(session).block(callback.from_user.id, target)
    RecommendationService(session, weights=settings.matching_weights).remove_candidate(callback.from_user.id, target)
    if threshold_reached:
        for admin_id in settings.admin_ids:
            await NotificationService(callback.bot).safe_send(
                admin_id, f"⚠️ Анкета <code>{target}</code> автоматически снята с публикации: достигнут порог жалоб."
            )
    await callback.message.edit_text("✅ Жалоба отправлена модераторам." if created else "Эта жалоба уже была учтена.")
    await callback.answer("Спасибо за помощь")
