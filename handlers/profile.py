from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.registration import start_registration
from keyboards.menu import MENU_PROFILE_LABELS, main_menu
from keyboards.profile import failed_photo_keyboard, photo_management_keyboard, photo_upload_keyboard, profile_keyboard
from middlewares.i18n import normalize_locale
from models import ModerationStatus, User, UserStatus
from services.interest_normalizer import format_interests
from services.localization import LocalizationService
from services.photo_analysis_progress import dismiss_photo_analysis_progress, show_photo_analysis_progress
from services.photo_moderation_service import RED, YELLOW, PhotoModerationError, PhotoModerationService, moderation_zone
from services.photo_upload_lock import PhotoUploadBusyError, photo_upload_lock
from services.profile_service import ProfileService
from states.profile_photo import ProfilePhotoState
from utils.document_links import documents_keyboard
from utils.legal import CONSENT_KEY
from utils.profile_media import ordered_photo_ids, send_profile_gallery
from utils.text import escape_html

router = Router()
localizer = LocalizationService()


def _accepts_confessions(user: User | None) -> bool:
    return user.accepts_confessions if user else True


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
    try:
        if message.photo:
            await message.edit_caption(caption=text, reply_markup=reply_markup)
        else:
            await message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest as exc:
        if "message is not modified" not in str(exc).lower():
            raise


async def _safe_edit_reply_markup(message: Message, reply_markup: InlineKeyboardMarkup) -> None:
    try:
        await message.edit_reply_markup(reply_markup=reply_markup)
    except TelegramBadRequest as exc:
        if "message is not modified" not in str(exc).lower():
            raise


def _profile_description(profile, locale: str = "ru") -> str:
    verification_key = "profile_verified" if profile.verification_status.value == "VERIFIED" else "profile_unverified"
    verification = LocalizationService().get(verification_key, locale)
    description = (
        f"{escape_html(profile.name)}, {profile.age}\n"
        f"📍 {escape_html(profile.district)}\n"
        f"🏫 {escape_html(profile.institution)}\n"
        f"🎯 {escape_html(format_interests(profile.interests))}\n\n"

        f"{escape_html(profile.bio)}\n\n"
        f"{verification}"
    )
    if profile.moderation_locked or profile.moderation_status.value == "UNDER_REVIEW":
        description += "\n" + LocalizationService().get("profile_moderation_hidden", locale)
    return description


async def _render_profile_message(
    message: Message, profile, *, accepts_confessions: bool = True, locale: str = "ru"
) -> None:
    hidden_by_moderation = (
        profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW
    )
    await _update_message_text(
        message,
        _profile_description(profile, locale),
        reply_markup=profile_keyboard(
            profile.is_visible and not hidden_by_moderation,
            hidden_by_moderation=hidden_by_moderation,
            accepts_confessions=accepts_confessions,
            locale=locale,
        ),
    )


async def show_profile(
    message: Message, user_id: int, session: AsyncSession, state: FSMContext, locale: str = "ru"
) -> None:
    """Show the same profile screen for reply and inline menu actions."""
    user = await session.get(User, user_id)
    if user is not None and user.status in {UserStatus.SUSPENDED, UserStatus.BANNED}:
        await message.answer(
            "⏸️ Ваша анкета временно ограничена или заблокирована. "
            "Нажмите «🆘 Апелляция», чтобы описать ситуацию и запросить пересмотр."
        )
        return
    service = ProfileService(session)
    p = await service.get_profile(user_id)
    if not p:
        if not (await state.get_data()).get(CONSENT_KEY, False):
            await message.answer(
                "⚠️ Для создания анкеты сначала ознакомьтесь с документами MeAnima.",
                reply_markup=documents_keyboard(
                    "terms",
                    "privacy",
                    "community",
                    "safety",
                    "moderation",
                    "alpha",
                    include_continue=True,
                ),
            )
            return
        await start_registration(message, state)
        return
    hidden_by_moderation = p.moderation_locked or p.moderation_status == ModerationStatus.UNDER_REVIEW
    await send_profile_gallery(
        message,
        p,
        _profile_description(p, locale),
        profile_keyboard(
            p.is_visible and not hidden_by_moderation,
            hidden_by_moderation=hidden_by_moderation,
            accepts_confessions=_accepts_confessions(user),
            locale=locale,
        ),
    )


@router.message(F.text.in_(MENU_PROFILE_LABELS))
async def profile(message: Message, session: AsyncSession, state: FSMContext, locale: str = "ru") -> None:
    await show_profile(message, message.from_user.id, session, state, locale)


@router.callback_query(F.data == "profile:language")
async def choose_language(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer(
        "🌐 Выберите язык / Alege limba:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language:set:ru")],
            [InlineKeyboardButton(text="🇲🇩 Română", callback_data="language:set:ro")],
        ]),
    )


@router.callback_query(F.data.startswith("language:set:"))
async def set_language(callback: CallbackQuery, session: AsyncSession) -> None:
    locale = normalize_locale(callback.data.rsplit(":", 1)[-1])
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer(localizer.get("profile_not_found", locale), show_alert=True)
        return
    profile.locale = locale
    await session.flush()
    await callback.answer(localizer.get("language_saved", locale))
    await callback.message.answer(
        localizer.get("language_saved", locale),
        reply_markup=main_menu(locale),
    )


@router.callback_query(F.data == "promo:my_profile")
async def promo_my_profile(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext, locale: str = "ru"
) -> None:
    await callback.answer()
    if locale == "ru":
        await show_profile(callback.message, callback.from_user.id, session, state)
    else:
        await show_profile(callback.message, callback.from_user.id, session, state, locale)


@router.callback_query(F.data == "profile:blocked")
async def profile_blocked(callback: CallbackQuery) -> None:
    await callback.answer(
        "🚫 Анкета скрыта модерацией или находится на проверке. "
        "Перейдите в «🆘 Апелляция», если хотите запросить пересмотр.",
        show_alert=True,
    )


@router.callback_query(F.data == "profile:confessions_toggle")
async def toggle_confessions(callback: CallbackQuery, session: AsyncSession) -> None:
    user = await session.get(User, callback.from_user.id)
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if user is None or profile is None:
        await callback.answer("Сначала создайте анкету.", show_alert=True)
        return
    user.accepts_confessions = not user.accepts_confessions
    await session.flush()
    hidden_by_moderation = profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW
    await _safe_edit_reply_markup(
        callback.message,
        profile_keyboard(
            profile.is_visible and not hidden_by_moderation,
            hidden_by_moderation=hidden_by_moderation,
            accepts_confessions=user.accepts_confessions,
        ),
    )
    await callback.answer("Признания включены." if user.accepts_confessions else "Признания отключены.")


@router.callback_query(F.data == "profile:create")
async def create_profile(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await callback.answer()
    if not (await state.get_data()).get(CONSENT_KEY, False):
        await callback.message.answer(
            "⚠️ Для создания анкеты сначала ознакомьтесь с документами MeAnima.",
            reply_markup=documents_keyboard(
                "terms",
                "privacy",
                "community",
                "safety",
                "moderation",
                "alpha",
                include_continue=True,
            ),
        )
        return
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
    await _safe_edit_reply_markup(callback.message, photo_management_keyboard(len(updated.photo_file_ids)))


@router.callback_query(F.data.startswith("photo:move:"))
async def move_photo(callback: CallbackQuery, session: AsyncSession) -> None:
    try:
        _, _, raw_index, raw_direction = (callback.data or "").split(":")
        direction = int(raw_direction)
    except ValueError:
        await callback.answer("Некорректная фотография.", show_alert=True)
        return
    if direction not in {-1, 1}:
        await callback.answer("Некорректное направление.", show_alert=True)
        return
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, raw_index) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась.", show_alert=True)
        return
    await ProfileService(session).move_photo(callback.from_user.id, photo_id, direction)
    updated = await ProfileService(session).get_profile(callback.from_user.id)
    await callback.answer("↔️ Порядок фотографий обновлён")
    await _safe_edit_reply_markup(callback.message, photo_management_keyboard(len(updated.photo_file_ids)))


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
    try:
        _, _, raw_index = (callback.data or "").split(":")
        int(raw_index)
    except ValueError:
        await callback.answer("Некорректная фотография.", show_alert=True)
        return
    await state.update_data(photo_action="replace", photo_index=raw_index)
    await state.set_state(ProfilePhotoState.waiting_photo)
    await _update_message_text(callback.message, "📸 Отправьте новую фотографию.", reply_markup=None)
    await callback.answer()


@router.message(ProfilePhotoState.waiting_photo, F.photo)
async def save_changed_photo(message: Message, state: FSMContext, session: AsyncSession, settings) -> None:
    try:
        async with photo_upload_lock(message.bot, message.from_user.id):
            data = await state.get_data()
            profile_service = ProfileService(session)
            profile = await profile_service.get_profile(message.from_user.id)
            if profile is None:
                await state.clear()
                return
            photo_id = message.photo[-1].file_id
            progress = await show_photo_analysis_progress(message)
            try:
                old_photo_id = None
                if data.get("photo_action") == "replace":
                    old_id = _photo_at(profile, str(data.get("photo_index")))
                    if old_id is None:
                        await dismiss_photo_analysis_progress(progress)
                        await message.answer("Список фото изменился. Откройте управление снова.")
                        await state.clear()
                        return
                    old_photo_id = old_id
                    await profile_service.replace_photo(message.from_user.id, old_id, photo_id)
                else:
                    await profile_service.add_photo(message.from_user.id, photo_id)
                assessment = await PhotoModerationService(
                    session, nsfw_threshold=settings.nsfw_threshold, settings=settings, bot=message.bot
                ).inspect(message.from_user.id, photo_id, defer_no_face_review=True)
            except ValueError as error:
                await dismiss_photo_analysis_progress(progress)
                await message.answer(str(error))
            except PhotoModerationError:
                await dismiss_photo_analysis_progress(progress)
                await message.answer(localizer.get("photo_check_error", profile.locale))
            else:
                await dismiss_photo_analysis_progress(progress)
                photo_zone = moderation_zone(assessment, nsfw_red_threshold=settings.nsfw_threshold)
                if photo_zone == RED:
                    if old_photo_id is None:
                        await profile_service.remove_photo(message.from_user.id, photo_id)
                    else:
                        await profile_service.replace_photo(message.from_user.id, photo_id, old_photo_id)
                    await state.update_data(
                        failed_photo_id=photo_id,
                        failed_photo_action=data.get("photo_action"),
                        failed_original_id=old_photo_id,
                    )
                    await state.set_state(ProfilePhotoState.awaiting_manual_review)
                    await message.answer(
                        localizer.get("photo_red", profile.locale),
                        reply_markup=failed_photo_keyboard(profile.locale),
                    )
                    return
                updated_profile = await profile_service.get_profile(message.from_user.id)
                if photo_zone == YELLOW:
                    await message.answer(localizer.get("photo_yellow", profile.locale))
                if data.get("photo_action") == "add" and updated_profile and len(updated_profile.photo_file_ids) < 3:
                    await message.answer(
                        localizer.format(
                            "photo_saved_count", profile.locale, count=len(updated_profile.photo_file_ids)
                        ),
                        reply_markup=photo_upload_keyboard("photo:done"),
                    )
                    return
                await message.answer(
                    localizer.get("photo_saved", profile.locale),
                    reply_markup=(
                        photo_management_keyboard(len(updated_profile.photo_file_ids)) if updated_profile else None
                    ),
                )
                await state.clear()
    except PhotoUploadBusyError:
        await message.answer("⏳ Фото ещё обрабатываются. Попробуйте отправить фото ещё раз через секунду.")


@router.callback_query(ProfilePhotoState.awaiting_manual_review, F.data == "photo:retry_failed")
async def retry_failed_photo(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ProfilePhotoState.waiting_photo)
    await callback.message.answer("📸 Отправьте другую фотографию.")
    await callback.answer()


@router.callback_query(ProfilePhotoState.awaiting_manual_review, F.data == "photo:review_failed")
async def review_failed_photo(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession, settings
) -> None:
    data = await state.get_data()
    photo_id = data.get("failed_photo_id")
    action = data.get("failed_photo_action")
    original_id = data.get("failed_original_id")
    profile_service = ProfileService(session)
    profile = await profile_service.get_profile(callback.from_user.id)
    if not photo_id or action not in {"add", "replace"} or profile is None:
        await state.clear()
        await callback.answer("Фото уже нельзя отправить на проверку. Загрузите его заново.", show_alert=True)
        return
    try:
        if action == "add":
            await profile_service.add_photo(callback.from_user.id, photo_id)
        elif not original_id:
            raise ValueError("Исходная фотография недоступна")
        else:
            await profile_service.replace_photo(callback.from_user.id, original_id, photo_id)
        assessment = await PhotoModerationService(
            session, nsfw_threshold=settings.nsfw_threshold, settings=settings, bot=callback.bot
        ).inspect(callback.from_user.id, photo_id)
    except PhotoModerationError:
        await state.clear()
        await callback.message.answer(localizer.get("photo_manual_submitted", profile.locale))
        await callback.answer()
        return
    except ValueError:
        await state.clear()
        await callback.message.answer("⚠️ Не удалось отправить это фото. Загрузите его ещё раз.")
        await callback.answer()
        return
    await state.clear()
    photo_zone = moderation_zone(assessment, nsfw_red_threshold=settings.nsfw_threshold)
    if photo_zone == RED:
        await callback.message.answer(localizer.get("photo_manual_submitted", profile.locale))
    elif photo_zone == YELLOW:
        await callback.message.answer(localizer.get("photo_yellow", profile.locale))
    else:
        await callback.message.answer(localizer.get("photo_saved", profile.locale))
    await callback.answer()


@router.message(ProfilePhotoState.waiting_photo)
async def changed_photo_not_photo(message: Message) -> None:
    await message.answer("Нужно отправить фотографию.")


@router.callback_query(F.data == "photo:done")
async def finish_photo_management(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext, locale: str = "ru"
) -> None:
    await state.clear()
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.message.answer(
            LocalizationService().get("verification_home", locale), reply_markup=main_menu(locale)
        )
        await callback.answer()
        return
    user = await session.get(User, callback.from_user.id)
    hidden_by_moderation = profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW
    await _update_message_text(
        callback.message,
        _profile_description(profile, locale),
        reply_markup=profile_keyboard(
            profile.is_visible and not hidden_by_moderation,
            hidden_by_moderation=hidden_by_moderation,
            accepts_confessions=_accepts_confessions(user),
            locale=locale,
        ),
    )
    await callback.answer()


@router.callback_query(F.data == "profile:toggle")
async def toggle(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    p = await service.get_profile(callback.from_user.id)
    if not p:
        await callback.answer()
        return
    user = await session.get(User, callback.from_user.id)
    if (
        p.moderation_locked
        or p.moderation_status == ModerationStatus.UNDER_REVIEW
        or (user is not None and user.status in {UserStatus.SUSPENDED, UserStatus.BANNED})
    ):
        await callback.answer("Анкета скрыта модерацией. Подайте апелляцию или дождитесь решения.", show_alert=True)
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
    await _safe_edit_reply_markup(
        callback.message,
        profile_keyboard(True, hidden_by_moderation=False, accepts_confessions=_accepts_confessions(user)),
    )
    await callback.answer("👀 Анкета снова видна")


@router.callback_query(F.data == "profile:toggle_confirm")
async def toggle_confirm(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    p = await service.get_profile(callback.from_user.id)
    if not p:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    user = await session.get(User, callback.from_user.id)
    if (
        p.moderation_locked
        or p.moderation_status == ModerationStatus.UNDER_REVIEW
        or (user is not None and user.status in {UserStatus.SUSPENDED, UserStatus.BANNED})
    ):
        await callback.answer("Анкета уже скрыта модерацией и не может быть опубликована.", show_alert=True)
        return
    p.is_visible = False
    await session.flush()
    await _update_message_text(
        callback.message,
        "🙈 Анкета скрыта. Нажмите «👀 Показать анкету», чтобы снова показать её.",
        reply_markup=profile_keyboard(
            False, hidden_by_moderation=False, accepts_confessions=_accepts_confessions(user)
        ),
    )
    await callback.answer("Анкета скрыта")


@router.callback_query(F.data == "profile:toggle_confirm_cancel")
async def toggle_confirm_cancel(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    user = await session.get(User, callback.from_user.id)
    await _render_profile_message(
        callback.message, profile, accepts_confessions=_accepts_confessions(user), locale=profile.locale or "ru"
    )
    await callback.answer("Скрытие отменено")


@router.callback_query(F.data == "profile:pause")
async def pause(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    try:
        await service.pause(callback.from_user.id)
    except ValueError:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    user = await session.get(User, callback.from_user.id)
    await _safe_edit_reply_markup(
        callback.message,
        profile_keyboard(False, hidden_by_moderation=False, accepts_confessions=_accepts_confessions(user)),
    )
    await callback.answer("Анкета на паузе")


@router.callback_query(F.data == "profile:delete")
async def delete(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    await _update_message_text(
        callback.message,
        "🗑 Вы уверены, что хотите удалить анкету? Это действие нельзя отменить.\n\n"
        "После удаления профиль и связанные данные будут удалены по правилам конфиденциальности.",
        reply_markup=_confirm_keyboard("Да, удалить", "profile:delete_confirm"),
    )
    await callback.answer()


@router.callback_query(F.data == "profile:delete_confirm")
async def delete_confirm(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    if not await service.delete(callback.from_user.id):
        await callback.answer("Анкета уже была удалена.", show_alert=True)
        return
    await _update_message_text(callback.message, "✅ Анкета удалена.")
    await callback.answer()


@router.callback_query(F.data == "profile:delete_confirm_cancel")
async def delete_confirm_cancel(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    user = await session.get(User, callback.from_user.id)
    await _render_profile_message(
        callback.message, profile, accepts_confessions=_accepts_confessions(user), locale=profile.locale or "ru"
    )
    await callback.answer("Удаление отменено")
