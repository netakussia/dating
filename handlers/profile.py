from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.profile import profile_keyboard
from repositories.profile import ProfileRepository
from handlers.registration import ask_gender
from aiogram.fsm.context import FSMContext

router = Router()
@router.message(F.text == "👤 Моя анкета")
async def profile(message: Message, session: AsyncSession, state: FSMContext) -> None:
    p = await ProfileRepository(session).by_user_id(message.from_user.id)
    if not p: await ask_gender(message, state); return
    caption = f"{p.name}, {p.age}\n📍 {p.district}\n🏫 {p.institution}\n🎯 {', '.join(p.interests)}\n\n{p.bio}"
    await message.answer_photo(p.photo_file_id, caption=caption, reply_markup=profile_keyboard(p.is_visible))
@router.callback_query(F.data == "profile:toggle")
async def toggle(callback: CallbackQuery, session: AsyncSession) -> None:
    p = await ProfileRepository(session).by_user_id(callback.from_user.id)
    if not p:
        await callback.answer()
        return
    if p.moderation_locked:
        await callback.answer("Анкета приостановлена модерацией. Подайте апелляцию.", show_alert=True)
        return
    p.is_visible = not p.is_visible
    await callback.message.edit_reply_markup(reply_markup=profile_keyboard(p.is_visible))
    await callback.answer("Видимость изменена")
