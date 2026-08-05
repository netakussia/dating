from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.registration import start_registration
from keyboards.profile import photo_management_keyboard, profile_keyboard
from services.photo_moderation_service import PhotoModerationError, PhotoModerationService
from services.profile_service import ProfileService
from states.profile_photo import ProfilePhotoState
from utils.profile_media import ordered_photo_ids, send_profile_gallery

router = Router()


@router.message(F.text == "👤 Моя анкета")
async def profile(message: Message, session: AsyncSession, state: FSMContext) -> None:
    service = ProfileService(session)
    p = await service.get_profile(message.from_user.id)
    if not p:
        await start_registration(message, state)
        return
    caption = f"{p.name}, {p.age}\n📍 {p.district}\n🏫 {p.institution}\n🎯 {', '.join(p.interests)}\n\n{p.bio}"
    verification = "🟢 Проверенный" if p.verification_status.value == "VERIFIED" else "⚪ Непроверенный"
    caption += f"\n\n{verification}"
    await send_profile_gallery(message, p, caption, profile_keyboard(p.is_visible))


@router.callback_query(F.data == "profile:create")
async def create_profile(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await start_registration(callback.message, state)


@router.callback_query(F.data == "profile:photos")
async def manage_photos(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Сначала создайте анкету.", show_alert=True)
        return
    photos = ordered_photo_ids(profile)
    await callback.message.answer(
        "Главная фотография показывается первой. Меняйте порядок, удаляйте или заменяйте фото.",
        reply_markup=photo_management_keyboard(len(photos)),
    )
    await callback.answer()


def _photo_at(profile, raw_index: str) -> str | None:
    try:
        return ordered_photo_ids(profile)[int(raw_index)]
    except (IndexError, ValueError):
        return None


@router.callback_query(F.data.startswith("photo:main:"))
async def set_main_photo(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, (callback.data or "").rsplit(":", 1)[-1]) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась. Откройте управление снова.", show_alert=True)
        return
    await ProfileService(session).move_photo(
        callback.from_user.id, photo_id, -ordered_photo_ids(profile).index(photo_id)
    )
    await callback.answer("Главная фотография обновлена")
    updated = await ProfileService(session).get_profile(callback.from_user.id)
    await callback.message.answer(
        "Главная фотография обновлена.", reply_markup=photo_management_keyboard(len(updated.photo_file_ids))
    )


@router.callback_query(F.data.startswith("photo:move:"))
async def move_photo(callback: CallbackQuery, session: AsyncSession) -> None:
    _, _, raw_index, raw_direction = (callback.data or "").split(":")
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, raw_index) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась.", show_alert=True)
        return
    await ProfileService(session).move_photo(callback.from_user.id, photo_id, int(raw_direction))
    await callback.answer("Порядок обновлён")
    updated = await ProfileService(session).get_profile(callback.from_user.id)
    await callback.message.answer(
        "Порядок обновлён.", reply_markup=photo_management_keyboard(len(updated.photo_file_ids))
    )


@router.callback_query(F.data.startswith("photo:delete:"))
async def delete_photo(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, (callback.data or "").rsplit(":", 1)[-1]) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась.", show_alert=True)
        return
    if len(ordered_photo_ids(profile)) == 1:
        await callback.answer("В анкете должна остаться хотя бы одна фотография.", show_alert=True)
        return
    await ProfileService(session).remove_photo(callback.from_user.id, photo_id)
    await callback.answer("Фотография удалена")
    updated = await ProfileService(session).get_profile(callback.from_user.id)
    await callback.message.answer(
        "Фотография удалена.", reply_markup=photo_management_keyboard(len(updated.photo_file_ids))
    )


@router.callback_query(F.data.startswith(("photo:replace:", "photo:add")))
async def request_photo(callback: CallbackQuery, state: FSMContext) -> None:
    action, _, raw_index = (callback.data or "photo:add:").partition(":")
    if action == "photo":
        action, _, raw_index = raw_index.partition(":")
    await state.update_data(photo_action=action, photo_index=raw_index or None)
    await state.set_state(ProfilePhotoState.waiting_photo)
    await callback.message.answer("Отправьте новую фотографию.")
    await callback.answer()


@router.message(ProfilePhotoState.waiting_photo, F.photo)
async def save_changed_photo(message: Message, state: FSMContext, session: AsyncSession, settings) -> None:
    data = await state.get_data()
    profile_service = ProfileService(session)
    profile = await profile_service.get_profile(message.from_user.id)
    if profile is None:
        await state.clear()
        return
    photo_id = message.photo[-1].file_id
    try:
        if data.get("photo_action") == "replace":
            old_id = _photo_at(profile, str(data.get("photo_index")))
            if old_id is None:
                await message.answer("Список фото изменился. Откройте управление снова.")
                return
            await profile_service.replace_photo(message.from_user.id, old_id, photo_id)
        else:
            await profile_service.add_photo(message.from_user.id, photo_id)
        await PhotoModerationService(
            session, nsfw_threshold=settings.nsfw_threshold, settings=settings, bot=message.bot
        ).inspect(message.from_user.id, photo_id)
    except PhotoModerationError:
        await message.answer("⚠️ Не удалось проверить фото. Анкета скрыта и отправлена модераторам.")
    else:
        await message.answer("✅ Фотография сохранена.")
    await state.clear()


@router.message(ProfilePhotoState.waiting_photo)
async def changed_photo_not_photo(message: Message) -> None:
    await message.answer("Нужно отправить фотографию.")


@router.callback_query(F.data == "photo:done")
async def finish_photo_management(callback: CallbackQuery) -> None:
    await callback.message.answer("Изменения фотографий сохранены.")
    await callback.answer()


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
