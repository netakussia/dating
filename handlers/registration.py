from __future__ import annotations

from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.profile_dto import ProfileDraft
from keyboards.dating import choice_keyboard
from keyboards.profile import registration_preview_keyboard
from services.localization import LocalizationService
from services.profile_service import ProfileService
from services.photo_moderation_service import PhotoModerationService
from states.registration import RegistrationState
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


async def _show_step(message: Message | CallbackQuery, state: FSMContext, step: str) -> None:
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(message)
    if step == "gender":
        await _set_step(state, "gender")
        await message.answer(
            localizer.get("registration_step_gender", locale=locale),
            reply_markup=choice_keyboard("reg_gender", [("Парень", "MALE"), ("Девушка", "FEMALE")]),
        )
    elif step == "target_gender":
        await _set_step(state, "target_gender")
        await message.answer(
            localizer.get("registration_step_target_gender", locale=locale),
            reply_markup=choice_keyboard("reg_target", [("Парней", "MALE"), ("Девушек", "FEMALE"), ("Не важно", "ALL")]),
        )
    elif step == "name":
        await _set_step(state, "name")
        await message.answer(localizer.get("registration_step_name", locale=locale))
    elif step == "age":
        await _set_step(state, "age")
        await message.answer(localizer.get("registration_step_age", locale=locale))
    elif step == "district":
        await _set_step(state, "district")
        await message.answer(localizer.get("registration_step_district", locale=locale))
    elif step == "institution":
        await _set_step(state, "institution")
        await message.answer(localizer.get("registration_step_institution", locale=locale))
    elif step == "interests":
        await _set_step(state, "interests")
        await message.answer(localizer.get("registration_step_interests", locale=locale))
    elif step == "bio":
        await _set_step(state, "bio")
        await message.answer(localizer.get("registration_step_bio", locale=locale))
    elif step == "photo":
        await _set_step(state, "photo")
        await message.answer(localizer.get("registration_step_photo", locale=locale))
    elif step == "preview":
        await _set_step(state, "preview")
        await _render_preview(message, state)


async def _render_preview(message: Message | CallbackQuery, state: FSMContext) -> None:
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(message)
    photo_ids = list(draft.get("photo_file_ids") or [])
    caption = (
        f"{draft.get('name') or '—'}, {draft.get('age') or '—'}\n"
        f"📍 {draft.get('district') or '—'}\n"
        f"🏫 {draft.get('institution') or '—'}\n"
        f"🎯 {', '.join(draft.get('interests', [])) or '—'}\n\n"
        f"{draft.get('bio') or '—'}"
    )
    if photo_ids:
        await message.answer_photo(photo_ids[0], caption=caption, reply_markup=registration_preview_keyboard())
    else:
        await message.answer(localizer.get("registration_step_preview", locale=locale), reply_markup=registration_preview_keyboard())
        await message.answer(caption)


async def start_registration(message: Message, state: FSMContext, *, edit: bool = False) -> None:
    draft = await _get_draft(state)
    draft.setdefault("locale", _language_code(message))
    draft.setdefault("is_visible", True)
    draft.setdefault("photo_file_ids", [])
    draft.setdefault("extra_data", {})
    await state.update_data(draft=draft)
    await state.clear()
    await state.update_data(draft=draft)
    if edit:
        await state.update_data(edit_mode=True)
    else:
        await state.update_data(edit_mode=False)
    await _show_step(message, state, "gender")


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
async def edit_profile(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await start_registration(callback.message, state, edit=True)


@router.callback_query(RegistrationState.gender, F.data.startswith("reg_gender:"))
async def gender(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.split(":", 1)[1]
    await _set_draft(state, gender=value)
    await _show_step(callback.message, state, "target_gender")
    await callback.answer()


@router.callback_query(RegistrationState.target_gender, F.data.startswith("reg_target:"))
async def target(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.split(":", 1)[1]
    await _set_draft(state, target_gender=value)
    await _show_step(callback.message, state, "name")
    await callback.answer()


@router.message(RegistrationState.name)
async def name(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(message)
    if not 2 <= len(value) <= 32:
        await message.answer(localizer.get("registration_step_name", locale=locale))
        return
    await _set_draft(state, name=value)
    await _show_step(message, state, "age")


@router.message(RegistrationState.age)
async def age(message: Message, state: FSMContext) -> None:
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(message)
    try:
        value = int((message.text or "").strip())
    except (TypeError, ValueError):
        await message.answer(localizer.get("registration_step_age", locale=locale))
        return
    if not 16 <= value <= 99:
        await message.answer(localizer.get("registration_step_age", locale=locale))
        return
    await _set_draft(state, age=value)
    await _show_step(message, state, "district")


@router.message(RegistrationState.district)
async def district(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(message)
    if len(value) > 64:
        await message.answer(localizer.get("registration_step_district", locale=locale))
        return
    await _set_draft(state, district=value)
    await _show_step(message, state, "institution")


@router.message(RegistrationState.institution)
async def institution(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(message)
    if not 3 <= len(value) <= 64:
        await message.answer(localizer.get("registration_step_institution", locale=locale))
        return
    await _set_draft(state, institution=value)
    await _show_step(message, state, "interests")


@router.message(RegistrationState.interests)
async def interests(message: Message, state: FSMContext) -> None:
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(message)
    value = (message.text or "").strip()
    if not value:
        await message.answer(localizer.get("registration_step_interests", locale=locale))
        return
    await _set_draft(state, interests=value)
    await _show_step(message, state, "bio")


@router.message(RegistrationState.bio)
async def bio(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(message)
    if not 10 <= len(value) <= 500:
        await message.answer(localizer.get("registration_step_bio", locale=locale))
        return
    await _set_draft(state, bio=value)
    await _show_step(message, state, "photo")


@router.message(RegistrationState.photo, F.photo)
async def photo(message: Message, state: FSMContext) -> None:
    draft = await _get_draft(state)
    photos = list(draft.get("photo_file_ids") or [])
    file_id = message.photo[-1].file_id
    if file_id not in photos:
        photos.append(file_id)
    if len(photos) > 3:
        photos = photos[:3]
    await _set_draft(state, photo_file_ids=photos, main_photo_file_id=photos[0] if photos else None)
    await _show_step(message, state, "preview")


@router.message(RegistrationState.photo)
async def non_photo(message: Message, state: FSMContext) -> None:
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(message)
    await message.answer(localizer.get("photo_required", locale=locale))


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
        interests=draft.get("interests") if isinstance(draft.get("interests"), list) else [draft.get("interests")],
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
    photo_moderation = PhotoModerationService(session, nsfw_threshold=settings.nsfw_threshold)
    for photo_file_id in payload.photo_file_ids:
        assessment = await photo_moderation.inspect(callback.from_user.id, photo_file_id)
        flagged_no_face = flagged_no_face or not assessment.face_detected
    await state.clear()
    if flagged_no_face:
        await callback.message.answer("⚠️ На фото не найдено лицо. Замените фотографию; анкета отправлена на проверку.")
    else:
        await callback.message.answer("✅ Анкета опубликована.")
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:edit")
async def preview_edit(callback: CallbackQuery, state: FSMContext) -> None:
    await _show_step(callback.message, state, "gender")
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:back")
async def preview_back(callback: CallbackQuery, state: FSMContext) -> None:
    previous = await _go_to_previous_step(state)
    await _show_step(callback.message, state, previous)
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:cancel")
async def preview_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer("Регистрация отменена.")
    await callback.answer()
