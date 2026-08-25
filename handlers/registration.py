from __future__ import annotations

from typing import Any

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.profile_dto import ProfileDraft
from keyboards.dating import choice_keyboard
from keyboards.menu import main_menu
from keyboards.profile import registration_preview_keyboard
from services.interest_normalizer import format_interests
from services.localization import LocalizationService
from services.photo_moderation_service import PhotoModerationError, PhotoModerationService
from services.profile_service import ProfileService
from states.registration import RegistrationState
from utils.document_links import documents_keyboard
from utils.legal import CONSENT_KEY
from utils.text import escape_html
from validators.profile_validator import ProfileValidationError

router = Router()
localizer = LocalizationService()

STEP_ORDER = [
    "gender",
    "target_gender",
    "name",
    "age",
    "district",
    "institution",
    "interests",
    "bio",
    "photo",
    "preview",
]
STATE_BY_STEP = {
    "gender": RegistrationState.gender,
    "target_gender": RegistrationState.target_gender,
    "name": RegistrationState.name,
    "age": RegistrationState.age,
    "district": RegistrationState.district,
    "institution": RegistrationState.institution,
    "interests": RegistrationState.interests,
    "bio": RegistrationState.bio,
    "photo": RegistrationState.photo,
    "preview": RegistrationState.preview,
}


def _language_code(message: Message | CallbackQuery | None) -> str:
    if message is None:
        return "ru"
    user = getattr(message, "from_user", None)
    code = getattr(user, "language_code", None)
    if not code:
        return "ru"
    return code.split("-")[0].lower() if "-" in code else code.lower()


async def _get_draft(state: FSMContext) -> dict[str, Any]:
    data = await state.get_data()
    draft = data.get("draft") or {}
    if "locale" not in draft:
        draft["locale"] = "ru"
    return draft


async def _set_draft(state: FSMContext, **updates: Any) -> None:
    draft = await _get_draft(state)
    draft.update(updates)
    await state.update_data(draft=draft)


async def _set_step(state: FSMContext, step: str) -> None:
    draft = await _get_draft(state)
    draft["step"] = step
    await state.update_data(draft=draft)
    await state.set_state(STATE_BY_STEP[step])


def _progress_bar(number: int, total: int) -> str:
    filled = "🟩" * number
    empty = "⬜" * (total - number)
    return f"{filled}{empty}"


def _step_prompt(step: str, locale: str) -> str:
    number = STEP_ORDER.index(step) + 1
    total = len(STEP_ORDER)
    bar = _progress_bar(number, total)
    return f"📝 Шаг {number}/{total}\n{bar}\n{localizer.get(f'registration_step_{step}', locale=locale)}"


async def _show_step(message: Message | CallbackQuery, state: FSMContext, step: str) -> None:
    target_msg = message.message if isinstance(message, CallbackQuery) else message
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(target_msg)
    if step == "gender":
        await _set_step(state, "gender")
        await target_msg.answer(
            _step_prompt("gender", locale),
            reply_markup=choice_keyboard("reg_gender", [("Парень", "MALE"), ("Девушка", "FEMALE")]),
        )
    elif step == "target_gender":
        await _set_step(state, "target_gender")
        await target_msg.answer(
            _step_prompt("target_gender", locale),
            reply_markup=choice_keyboard(
                "reg_target", [("Парней", "MALE"), ("Девушек", "FEMALE"), ("Не важно", "ALL")]
            ),
        )
    elif step in {"name", "age", "district", "institution", "interests", "bio", "photo"}:
        await _set_step(state, step)
        await target_msg.answer(_step_prompt(step, locale))
    elif step == "preview":
        await _set_step(state, "preview")
        await _render_preview(message, state)


async def _render_preview(message: Message | CallbackQuery, state: FSMContext) -> None:
    target_msg = message.message if isinstance(message, CallbackQuery) else message
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(target_msg)
    photo_ids = list(draft.get("photo_file_ids") or [])
    caption = (
        f"<b>{escape_html(draft.get('name') or '—')}</b>, {draft.get('age') or '—'}\n"
        f"📍 <code>{escape_html(draft.get('district') or '—')}</code>\n"
        f"🏫 <i>{escape_html(draft.get('institution') or '—')}</i>\n"
        f"🎯 {escape_html(format_interests(draft.get('interests')))}\n\n"

        f"{escape_html(draft.get('bio') or '—')}"
    )
    header = _step_prompt("preview", locale)
    if photo_ids:
        if len(photo_ids) == 1:
            await target_msg.answer_photo(
                photo_ids[0], caption=f"{header}\n{caption}", reply_markup=registration_preview_keyboard()
            )
            return
        media = [
            InputMediaPhoto(media=photo_id, caption=f"{header}\n{caption}" if index == 0 else None)
            for index, photo_id in enumerate(photo_ids)
        ]
        await target_msg.answer_media_group(media)
        await target_msg.answer("📋 Предпросмотр анкеты", reply_markup=registration_preview_keyboard())
        return
    await target_msg.answer(header, reply_markup=registration_preview_keyboard())
    await target_msg.answer(caption)


async def start_registration(
    message: Message, state: FSMContext, *, edit: bool = False, initial_draft: dict[str, Any] | None = None
) -> None:
    consent = bool((await state.get_data()).get(CONSENT_KEY, False))
    if not consent and not edit:
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
    draft = initial_draft or await _get_draft(state)
    draft.setdefault("locale", _language_code(message))
    draft.setdefault("is_visible", True)
    draft.setdefault("photo_file_ids", [])
    draft.setdefault("extra_data", {})
    draft.setdefault("photo_replacement_started", False)
    draft["legal_consent"] = consent
    await state.clear()
    await state.update_data(draft=draft, legal_consent=consent)
    if edit:
        await state.update_data(edit_mode=True)
    else:
        await state.update_data(edit_mode=False)
    await _show_step(message, state, "gender")


@router.message(
    StateFilter(RegistrationState),
    F.text.in_(
        {
            "💘 Знакомства",
            "💕 Мои симпатии",
            "👤 Моя анкета",
            "🛡 Верификация",
            "💌 Признание",
            "🆘 Апелляция",
            "❓ Помощь",
        }
    ),
)
async def handle_menu_buttons_during_registration(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu())


async def _go_to_previous_step(state: FSMContext) -> str:
    draft = await _get_draft(state)
    current = draft.get("step") or "gender"
    try:
        index = STEP_ORDER.index(current)
    except ValueError:
        return "gender"
    previous = STEP_ORDER[max(index - 1, 0)]
    return previous


async def _go_to_next_step(state: FSMContext) -> str:
    draft = await _get_draft(state)
    current = draft.get("step") or "gender"
    try:
        index = STEP_ORDER.index(current)
    except ValueError:
        return "preview"
    if index + 1 >= len(STEP_ORDER):
        return "preview"
    return STEP_ORDER[index + 1]


@router.callback_query(F.data == "profile:edit")
async def edit_profile(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await callback.answer()
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await start_registration(callback.message, state)
        return
    await start_registration(
        callback.message,
        state,
        edit=True,
        initial_draft={
            "gender": profile.gender.value,
            "target_gender": profile.target_gender.value,
            "name": profile.name,
            "age": profile.age,
            "district": profile.district,
            "institution": profile.institution,
            "interests": profile.interests,
            "bio": profile.bio,
            "photo_file_ids": list(profile.photo_file_ids or []),
            "main_photo_file_id": profile.main_photo_file_id,
            "locale": profile.locale,
            "is_visible": profile.is_visible,
            "extra_data": profile.extra_data or {},
        },
    )


@router.callback_query(RegistrationState.gender, F.data.startswith("reg_gender:"))
async def gender(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.split(":", 1)[1]
    await _set_draft(state, gender=value)
    await _show_step(callback, state, "target_gender")
    await callback.answer()


@router.callback_query(RegistrationState.target_gender, F.data.startswith("reg_target:"))
async def target(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.split(":", 1)[1]
    await _set_draft(state, target_gender=value)
    await _show_step(callback, state, "name")
    await callback.answer()


@router.message(RegistrationState.name)
async def name(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not 2 <= len(value) <= 32:
        await message.answer("⚠️ Имя должно содержать от 2 до 32 символов. Попробуйте ещё раз.")
        return
    await _set_draft(state, name=value)
    await _show_step(message, state, "age")


@router.message(RegistrationState.age)
async def age(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    try:
        value = int(text)
    except (TypeError, ValueError):
        await message.answer("⚠️ Укажите возраст числом от 16 до 99.")
        return
    if not 16 <= value <= 99:
        await message.answer("⚠️ Укажите возраст от 16 до 99 лет.")
        return
    await _set_draft(state, age=value)
    await _show_step(message, state, "district")


@router.message(RegistrationState.district)
async def district(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not value:
        await message.answer("⚠️ Укажите свой район.")
        return
    if len(value) > 64:
        await message.answer("⚠️ Район должен быть не длиннее 64 символов. Напишите ещё раз.")
        return
    await _set_draft(state, district=value)
    await _show_step(message, state, "institution")


@router.message(RegistrationState.institution)
async def institution(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not 3 <= len(value) <= 64:
        await message.answer("⚠️ Укажите место учебы или работы: 3–64 символа.")
        return
    await _set_draft(state, institution=value)
    await _show_step(message, state, "interests")


@router.message(RegistrationState.interests)
async def interests(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not value:
        await message.answer("⚠️ Напишите хотя бы одну интересную тему через запятую.")
        return
    await _set_draft(state, interests=value)
    await _show_step(message, state, "bio")


@router.message(RegistrationState.bio)
async def bio(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not 10 <= len(value) <= 500:
        await message.answer("⚠️ Напишите о себе 10–500 символов.")
        return
    await _set_draft(state, bio=value)
    await _show_step(message, state, "photo")


@router.message(RegistrationState.photo, F.photo)
async def photo(message: Message, state: FSMContext) -> None:
    draft = await _get_draft(state)
    photos = list(draft.get("photo_file_ids") or [])
    file_id = message.photo[-1].file_id
    replacing_photos = bool(
        draft.get("edit_mode") and draft.get("photo_file_ids") and not draft.get("photo_replacement_started")
    )
    if replacing_photos:
        photos = [file_id]
        await _set_draft(state, photo_replacement_started=True)
    elif file_id not in photos:
        photos.append(file_id)
    if len(photos) > 3:
        photos = photos[:3]
        await message.answer(
            "⚠️ Можно загрузить не более 3 фотографий. Сохранены первые три."
        )
    await _set_draft(state, photo_file_ids=photos, main_photo_file_id=photos[0] if photos else None)
    await _show_step(message, state, "preview")


@router.message(RegistrationState.photo)
async def non_photo(message: Message, state: FSMContext) -> None:
    await message.answer("⚠️ Отправьте фотографию, чтобы продолжить.")


@router.callback_query(RegistrationState.preview, F.data == "profile:rephoto")
async def preview_rephoto(callback: CallbackQuery, state: FSMContext) -> None:
    await _show_step(callback, state, "photo")
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:publish")
async def publish(callback: CallbackQuery, state: FSMContext, session: AsyncSession, settings) -> None:
    draft = await _get_draft(state)
    payload = ProfileDraft(
        gender=draft.get("gender"),
        target_gender=draft.get("target_gender"),
        name=draft.get("name"),
        age=draft.get("age"),
        district=draft.get("district"),
        institution=draft.get("institution"),
        interests=draft.get("interests"),
        bio=draft.get("bio"),
        photo_file_ids=list(draft.get("photo_file_ids") or []),
        main_photo_file_id=draft.get("main_photo_file_id"),
        locale=draft.get("locale") or "ru",
        is_visible=bool(draft.get("is_visible", True)),
        extra_data=draft.get("extra_data") or {},
    )
    profile_service = ProfileService(session)
    try:
        await profile_service.create_or_update(callback.from_user.id, payload)
    except ProfileValidationError as exc:
        details = "\n".join(f"- {message}" for message in exc.errors.values())
        await callback.message.answer(f"Проверьте анкету:\n{details}")
        await callback.answer("Данные анкеты не прошли проверку", show_alert=True)
        return
    flagged_no_face = False
    flagged_nsfw = False
    photo_moderation = PhotoModerationService(
        session, nsfw_threshold=settings.nsfw_threshold, settings=settings, bot=callback.bot
    )
    try:
        for photo_file_id in payload.photo_file_ids:
            assessment = await photo_moderation.inspect(callback.from_user.id, photo_file_id)
            flagged_no_face = flagged_no_face or not assessment.face_detected
            flagged_nsfw = flagged_nsfw or assessment.nsfw_score >= settings.nsfw_threshold
    except PhotoModerationError:
        await state.clear()
        await callback.message.answer("⚠️ Не удалось проверить фото. Анкета скрыта и отправлена модераторам.")
        await callback.answer()
        return
    await state.clear()
    if flagged_nsfw:
        await callback.message.answer(
            "⚠️ Фото отправлено на проверку модераторам. До решения анкета скрыта.\n"
            "Вы можете продолжить использование бота или заглянуть в «👤 Моя анкета».",
            reply_markup=main_menu(),
        )
    elif flagged_no_face:
        await callback.message.answer(
            "⚠️ На фото не найдено лицо. Замените фотографию в профиле; анкета отправлена на проверку.",
            reply_markup=main_menu(),
        )
    else:
        await callback.message.answer(
            "✅ Ваша анкета успешно опубликована!\n\n"
            "Теперь вы можете искать пару в разделе «💘 Знакомства» или настроить анкету в «👤 Моя анкета».",
            reply_markup=main_menu(),
        )
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:edit")
async def preview_edit(callback: CallbackQuery, state: FSMContext) -> None:
    await _show_step(callback, state, "gender")
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:back")
async def preview_back(callback: CallbackQuery, state: FSMContext) -> None:
    previous = await _go_to_previous_step(state)
    await _show_step(callback, state, previous)
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:cancel")
async def preview_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    msg = "❌ Регистрация отменена. Вы можете начать заново в любой момент через «👤 Моя анкета»."
    await callback.message.answer(msg, reply_markup=main_menu())
    await callback.answer()

