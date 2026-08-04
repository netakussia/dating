from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from config import Settings
from services.confession_service import ConfessionService
from states.confession import ConfessionState

router = Router()
@router.message(F.text == "💌 Признание")
async def begin(message: Message, state: FSMContext) -> None:
    await state.set_state(ConfessionState.recipient); await message.answer("Кому отправить признание? Введите @username.")
@router.message(ConfessionState.recipient)
async def recipient(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    valid_username = value.startswith("@") and 3 <= len(value) <= 33
    valid_id = value.isdigit() and 4 <= len(value) <= 20
    if not (valid_username or valid_id):
        await message.answer("Введите корректный @username или числовой Telegram ID.")
        return
    await state.update_data(recipient=value); await state.set_state(ConfessionState.text); await message.answer("Введите текст (5–1000 символов).")
@router.message(ConfessionState.text)
async def confirmation(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not 5 <= len(text) <= 1000: await message.answer("Текст должен быть 5–1000 символов."); return
    await state.update_data(text=text)
    kb = InlineKeyboardBuilder(); kb.button(text="✅ Отправить", callback_data="confession:send"); kb.button(text="Отмена", callback_data="confession:cancel"); kb.adjust(2)
    await state.set_state(ConfessionState.confirm)
    await message.answer("Проверьте текст. Отправитель не будет раскрыт:\n\n" + text, reply_markup=kb.as_markup())

@router.callback_query(ConfessionState.confirm, F.data == "confession:cancel")
async def cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear(); await callback.message.edit_text("Отправка отменена."); await callback.answer()

@router.callback_query(ConfessionState.confirm, F.data == "confession:send")
async def send(callback: CallbackQuery, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    data = await state.get_data(); recipient, text = data["recipient"], data["text"]
    confession = await ConfessionService(session, settings.daily_secret_salt).create(callback.from_user.id, recipient, text)
    if confession.recipient_id:
        await callback.bot.send_message(confession.recipient_id, f"💌 Вам анонимное признание:\n\n{text}")
        await callback.message.edit_text("✅ Признание доставлено анонимно.")
    else:
        link = f"https://t.me/{(await callback.bot.get_me()).username}?start=confession_{confession.id}"
        await callback.message.edit_text(f"Получатель ещё не запускал бота. Передайте ему ссылку: {link}")
    await state.clear()
    await callback.answer()
