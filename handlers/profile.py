from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.registration import start_registration
from keyboards.profile import profile_keyboard
from services.profile_service import ProfileService

router = Router()


@router.message(F.text == "👤 Моя анкета")
async def profile(message: Message, session: AsyncSession, state: FSMContext) -> None:
    service = ProfileService(session)
    p = await service.get_profile(message.from_user.id)
    if not p:
        await start_registration(message, state)
        return
    caption = f"{p.name}, {p.age}\n📍 {p.district}\n🏫 {p.institution}\n🎯 {', '.join(p.interests)}\n\n{p.bio}"
    await message.answer_photo(p.photo_file_id, caption=caption, reply_markup=profile_keyboard(p.is_visible))


@router.callback_query(F.data == "profile:toggle")
async def toggle(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    p = await service.get_profile(callback.from_user.id)
    if not p:
        await callback.answer()
        return
    if p.moderation_locked:
        await callback.answer("Анкета приостановлена модерацией. Подайте апелляцию.", show_alert=True)
        return
    p.is_visible = not p.is_visible
    await session.flush()
    await callback.message.edit_reply_markup(reply_markup=profile_keyboard(p.is_visible))
    await callback.answer("Видимость изменена")


@router.callback_query(F.data == "profile:pause")
async def pause(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    try:
        await service.pause(callback.from_user.id)
    except ValueError:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    await callback.message.edit_reply_markup(reply_markup=profile_keyboard(False))
    await callback.answer("Анкета на паузе")


@router.callback_query(F.data == "profile:delete")
async def delete(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    await service.delete(callback.from_user.id)
    await callback.message.answer("Анкета удалена")
    await callback.answer()
