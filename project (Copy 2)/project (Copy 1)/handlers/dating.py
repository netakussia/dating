from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.dating import dating_keyboard, report_reasons_keyboard
from services.match_service import MatchService
from services.recommendation import RecommendationService
from repositories.report import ReportRepository
from repositories.discovery import DiscoveryRepository
from models import ReportReason
from states.dating import DatingState
from utils.contacts import telegram_contact

router = Router()
async def show_next(message: Message, user_id: int, session: AsyncSession) -> None:
    p = await RecommendationService(session).next_profile(user_id)
    if not p: await message.answer("Сейчас новых анкет нет. Загляните позже."); return
    caption = f"{p.name}, {p.age}\n📍 {p.district}\n🏫 {p.institution}\n🎯 {', '.join(p.interests)}\n\n{p.bio}"
    await message.answer_photo(p.photo_file_id, caption=caption, reply_markup=dating_keyboard(p.user_id))
@router.message(F.text == "💘 Знакомства")
async def browse(message: Message, session: AsyncSession) -> None: await show_next(message, message.from_user.id, session)
@router.callback_query(F.data.startswith("like:"))
async def like(callback: CallbackQuery, session: AsyncSession) -> None:
    target = int(callback.data.split(":")[1])
    if target == callback.from_user.id: await callback.answer(); return
    _, mutual = await MatchService(session).like(callback.from_user.id, target)
    await callback.answer("Это взаимно! 🎉" if mutual else "Лайк отправлен ❤️")
    if mutual:
        target_profile, target_user = await DiscoveryRepository(session).profile_and_user(target)
        source_contact = telegram_contact(callback.from_user.id, callback.from_user.username, callback.from_user.full_name)
        target_contact = telegram_contact(
            target,
            target_user.username if target_user else None,
            target_profile.name if target_profile else "Пользователь",
        )
        await callback.bot.send_message(target, f"🎉 Взаимная симпатия! Контакт: {source_contact}")
        await callback.message.answer(f"🎉 Взаимная симпатия! Контакт: {target_contact}")
    else:
        await callback.bot.send_message(target, "❤️ Кому-то понравилась ваша анкета!")
    await show_next(callback.message, callback.from_user.id, session)

@router.callback_query(F.data.startswith("comment:"))
async def comment_start(callback: CallbackQuery, state: FSMContext) -> None:
    target = int(callback.data.split(":")[1])
    await state.update_data(like_target=target)
    await state.set_state(DatingState.like_comment)
    await callback.message.answer("Напишите короткое сообщение к лайку (до 200 символов).")
    await callback.answer()

@router.message(DatingState.like_comment)
async def comment_finish(message: Message, state: FSMContext, session: AsyncSession) -> None:
    text = (message.text or "").strip()
    if not 1 <= len(text) <= 200:
        await message.answer("Сообщение должно быть от 1 до 200 символов.")
        return
    target = (await state.get_data())["like_target"]
    _, mutual = await MatchService(session).like(message.from_user.id, target, text)
    await state.clear()
    await message.bot.send_message(target, "💌 Кто-то оставил лайк с сообщением:\n\n" + text)
    if mutual:
        target_profile, target_user = await DiscoveryRepository(session).profile_and_user(target)
        source_contact = telegram_contact(message.from_user.id, message.from_user.username, message.from_user.full_name)
        target_contact = telegram_contact(
            target,
            target_user.username if target_user else None,
            target_profile.name if target_profile else "Пользователь",
        )
        await message.bot.send_message(target, f"🎉 Взаимная симпатия! Контакт: {source_contact}")
        await message.answer(f"🎉 Взаимная симпатия! Контакт: {target_contact}")
    else:
        await message.answer("❤️ Лайк с сообщением отправлен.")
@router.callback_query(F.data.startswith("skip:"))
async def skip(callback: CallbackQuery, session: AsyncSession) -> None:
    target = int(callback.data.split(":")[1])
    await DiscoveryRepository(session).skip(callback.from_user.id, target)
    await callback.answer("Анкета больше не будет показана")
    await show_next(callback.message, callback.from_user.id, session)

@router.callback_query(F.data.startswith("block:"))
async def block(callback: CallbackQuery, session: AsyncSession) -> None:
    target = int(callback.data.split(":")[1])
    await DiscoveryRepository(session).block(callback.from_user.id, target)
    await callback.answer("Пользователь заблокирован")
    await show_next(callback.message, callback.from_user.id, session)

@router.callback_query(F.data.startswith("report:"))
async def report(callback: CallbackQuery, session: AsyncSession) -> None:
    target = int(callback.data.split(":")[1])
    await callback.message.answer("Выберите причину жалобы:", reply_markup=report_reasons_keyboard(target))
    await callback.answer()

@router.callback_query(F.data.startswith("report_reason:"))
async def report_reason(callback: CallbackQuery, session: AsyncSession) -> None:
    _, target, reason = callback.data.split(":")
    await ReportRepository(session).add(callback.from_user.id, int(target), ReportReason(reason))
    await callback.message.edit_text("✅ Жалоба отправлена модераторам.")
    await callback.answer("Спасибо за помощь")
