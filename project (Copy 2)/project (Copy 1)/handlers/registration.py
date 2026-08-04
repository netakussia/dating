from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.dating import choice_keyboard
from models import Gender, Profile
from repositories.profile import ProfileRepository
from states.registration import RegistrationState

router = Router()

async def ask_gender(message: Message, state: FSMContext) -> None:
    await state.set_state(RegistrationState.gender); await message.answer("Ваш пол?", reply_markup=choice_keyboard("reg_gender", [("Парень", "MALE"), ("Девушка", "FEMALE")]))

@router.callback_query(F.data == "profile:edit")
async def edit_profile(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(); await ask_gender(callback.message, state)

@router.callback_query(RegistrationState.gender, F.data.startswith("reg_gender:"))
async def gender(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(gender=callback.data.split(":")[1]); await state.set_state(RegistrationState.target_gender); await callback.message.answer("Кого ищете?", reply_markup=choice_keyboard("reg_target", [("Парней", "MALE"), ("Девушек", "FEMALE"), ("Не важно", "ALL")])); await callback.answer()

@router.callback_query(RegistrationState.target_gender, F.data.startswith("reg_target:"))
async def target(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(target_gender=callback.data.split(":")[1]); await state.set_state(RegistrationState.name); await callback.message.answer("Как вас зовут? (2–32 символа)"); await callback.answer()

@router.message(RegistrationState.name)
async def name(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not 2 <= len(value) <= 32: await message.answer("Введите имя от 2 до 32 символов."); return
    await state.update_data(name=value); await state.set_state(RegistrationState.age); await message.answer("Ваш возраст (14–99)?")

@router.message(RegistrationState.age)
async def age(message: Message, state: FSMContext) -> None:
    try: value = int(message.text)
    except (TypeError, ValueError): value = 0
    if not 14 <= value <= 99: await message.answer("Введите возраст числом от 14 до 99."); return
    await state.update_data(age=value); await state.set_state(RegistrationState.district); await message.answer("Ваш район?")

@router.message(RegistrationState.district)
async def district(message: Message, state: FSMContext) -> None:
    await state.update_data(district=(message.text or "").strip()); await state.set_state(RegistrationState.institution); await message.answer("Где учитесь/работаете? (3–64 символа)")

@router.message(RegistrationState.institution)
async def institution(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not 3 <= len(value) <= 64: await message.answer("Введите 3–64 символов."); return
    await state.update_data(institution=value); await state.set_state(RegistrationState.interests); await message.answer("Интересы через запятую (например: музыка, спорт, кино)")

@router.message(RegistrationState.interests)
async def interests(message: Message, state: FSMContext) -> None:
    values = [x.strip().lower() for x in (message.text or "").split(",") if x.strip()][:10]
    await state.update_data(interests=values); await state.set_state(RegistrationState.bio); await message.answer("Расскажите о себе (10–500 символов)")

@router.message(RegistrationState.bio)
async def bio(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not 10 <= len(value) <= 500: await message.answer("Нужно от 10 до 500 символов."); return
    await state.update_data(bio=value); await state.set_state(RegistrationState.photo); await message.answer("Отправьте фото.")

@router.message(RegistrationState.photo, F.photo)
async def photo(message: Message, state: FSMContext, session: AsyncSession) -> None:
    data = await state.get_data(); existing = await ProfileRepository(session).by_user_id(message.from_user.id)
    values = dict(data, user_id=message.from_user.id, photo_file_id=message.photo[-1].file_id, gender=Gender(data["gender"]), target_gender=Gender(data["target_gender"]))
    if existing:
        for key, value in values.items(): setattr(existing, key, value)
    else: session.add(Profile(**values))
    await state.clear(); await message.answer("✅ Анкета сохранена.")

@router.message(RegistrationState.photo)
async def non_photo(message: Message) -> None: await message.answer("Нужна фотография.")
