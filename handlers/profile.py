from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.registration import start_registration
from keyboards.profile import photo_management_keyboard, profile_keyboard
from services.interest_normalizer import format_interests
from services.photo_moderation_service import PhotoModerationError, PhotoModerationService
from services.profile_service import ProfileService
from states.profile_photo import ProfilePhotoState
from utils.profile_media import ordered_photo_ids, send_profile_gallery

router = Router()


def _photo_management_text() -> str:
    return (
        "📸 Управление фотографиями.\n"
        "Главная фотография будет показываться первой. Меняйте порядок, заменяйте или удаляйте фото."
    )


def _confirm_keyboard(yes_text: str, yes_data: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=yes_text, callback_data=yes_data),
            InlineKeyboardButton(text="❌ Отмена", callback_data=f"{yes_data}_cancel"),
        ]
    ])
    return kb


async def _update_message_text(message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None) -> None:
    if message.photo:
        await message.edit_caption(caption=text, reply_markup=reply_markup)
    else:
        await message.edit_text(text, reply_markup=reply_markup)


def _profile_description(profile) -> str:
    verification = "🟢 Проверенный" if profile.verification_status.value == "VERIFIED" else "⚪ Непроверенный"
    description = (
        f"{profile.name}, {profile.age}\n"
        f"📍 {profile.district}\n"
        f"🏫 {profile.institution}\n"
        f"🎯 {format_interests(profile.interests)}\n\n"

        f"{profile.bio}\n\n"
        f"{verification}"
    )
    if profile.moderation_locked or profile.moderation_status.value == "UNDER_REVIEW":
        description += "\n⏳ Анкета скрыта до решения модератора или замены фотографии."
    return description


async def _render_profile_message(message: Message, profile) -> None:
    await _update_message_text(
        message,
        _profile_description(profile),
        reply_markup=profile_keyboard(profile.is_visible),
    )


@router.message(F.text == "👤 Моя анкета")
async def profile(message: Message, session: AsyncSession, state: FSMContext) -> None:
    service = ProfileService(session)
    p = await service.get_profile(message.from_user.id)
    if not p:
        await start_registration(message, state)
        return
    await send_profile_gallery(message, p, _profile_description(p), profile_keyboard(p.is_visible))


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
    await _update_message_text(
        callback.message,
        _photo_management_text(),
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
    updated = await ProfileService(session).get_profile(callback.from_user.id)
    await callback.answer("⭐ Главная фотография обновлена")
    await callback.message.edit_reply_markup(reply_markup=photo_management_keyboard(len(updated.photo_file_ids)))


@router.callback_query(F.data.startswith("photo:move:"))
async def move_photo(callback: CallbackQuery, session: AsyncSession) -> None:
    _, _, raw_index, raw_direction = (callback.data or "").split(":")
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, raw_index) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась.", show_alert=True)
        return
    await ProfileService(session).move_photo(callback.from_user.id, photo_id, int(raw_direction))
    updated = await ProfileService(session).get_profile(callback.from_user.id)
    await callback.answer("↔️ Порядок фотографий обновлён")
    await callback.message.edit_reply_markup(reply_markup=photo_management_keyboard(len(updated.photo_file_ids)))


@router.callback_query(F.data.startswith("photo:delete:"))
async def delete_photo(callback: CallbackQuery, session: AsyncSession) -> None:
    raw_index = (callback.data or "").rsplit(":" , 1)[-1]
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, raw_index) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась.", show_alert=True)
        return
    if len(ordered_photo_ids(profile)) == 1:
        await callback.answer("В анкете должна остаться хотя бы одна фотография.", show_alert=True)
        return
    await _update_message_text(
        callback.message,
        "🗑 Вы уверены, что хотите удалить эту фотографию?",
        reply_markup=_confirm_keyboard("Да, удалить", f"photo:delete_confirm:{raw_index}"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("photo:delete_confirm:"))
async def delete_photo_confirm(callback: CallbackQuery, session: AsyncSession) -> None:
    raw_index = (callback.data or "").split(":", 2)[-1]
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, raw_index) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась.", show_alert=True)
        return
    if len(ordered_photo_ids(profile)) == 1:
        await callback.answer("В анкете должна остаться хотя бы одна фотография.", show_alert=True)
        return
    await ProfileService(session).remove_photo(callback.from_user.id, photo_id)
    updated = await ProfileService(session).get_profile(callback.from_user.id)
    await callback.answer("Фотография удалена")
    await _update_message_text(
        callback.message,
        _photo_management_text(),
        reply_markup=photo_management_keyboard(len(updated.photo_file_ids)),
    )


@router.callback_query(F.data == "photo:add")
async def request_add_photo(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(photo_action="add", photo_index=None)
    await state.set_state(ProfilePhotoState.waiting_photo)
    await _update_message_text(callback.message, "📸 Отправьте новую фотографию.", reply_markup=None)
    await callback.answer()


@router.callback_query(F.data.startswith("photo:replace:"))
async def request_replace_photo(callback: CallbackQuery, state: FSMContext) -> None:
    _, _, raw_index = (callback.data or "photo:replace:").split(":")
    await state.update_data(photo_action="replace", photo_index=raw_index)
    await state.set_state(ProfilePhotoState.waiting_photo)
    await _update_message_text(callback.message, "📸 Отправьте новую фотографию.", reply_markup=None)
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
                await state.clear()
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
    await _update_message_text(callback.message, "✅ Изменения фотографий сохранены.")
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
    if p.is_visible:
        await _update_message_text(
            callback.message,
            "🙈 Скрыть анкету? Она перестанет показываться другим пользователям до повторного включения.",
            reply_markup=_confirm_keyboard("Да, скрыть", "profile:toggle_confirm"),
        )
        await callback.answer()
        return
    p.is_visible = True
    await session.flush()
    await callback.message.edit_reply_markup(reply_markup=profile_keyboard(True))
    await callback.answer("👀 Анкета снова видна")


@router.callback_query(F.data == "profile:toggle_confirm")
async def toggle_confirm(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    p = await service.get_profile(callback.from_user.id)
    if not p:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    p.is_visible = False
    await session.flush()
    await _update_message_text(
        callback.message,
        "🙈 Анкета скрыта. Нажмите «👀 Показать анкету», чтобы снова показать её.",
        reply_markup=profile_keyboard(False),
    )
    await callback.answer("Анкета скрыта")


@router.callback_query(F.data == "profile:toggle_confirm_cancel")
async def toggle_confirm_cancel(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    await _render_profile_message(callback.message, profile)
    await callback.answer("Скрытие отменено")


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
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    await _update_message_text(
        callback.message,
        "🗑 Вы уверены, что хотите удалить анкету? Это действие нельзя отменить.",
        reply_markup=_confirm_keyboard("Да, удалить", "profile:delete_confirm"),
    )
    await callback.answer()


@router.callback_query(F.data == "profile:delete_confirm")
async def delete_confirm(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    await service.delete(callback.from_user.id)
    await _update_message_text(callback.message, "✅ Анкета удалена.")
    await callback.answer()


@router.callback_query(F.data == "profile:delete_confirm_cancel")
async def delete_confirm_cancel(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    await _render_profile_message(callback.message, profile)
    await callback.answer("Удаление отменено")
