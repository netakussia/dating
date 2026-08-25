from uuid import uuid4

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from keyboards.menu import main_menu
from services.confession_service import ConfessionService
from services.eligibility import EligibilityError, EligibilityService
from services.notification_service import NotificationService
from states.confession import ConfessionState
from utils.text import escape_html

router = Router()


@router.message(
    StateFilter(ConfessionState),
    F.text.in_({
        "💘 Знакомства",
        "💕 Мои симпатии",
        "👤 Моя анкета",
        "🛡 Верификация",
        "💌 Признание",
        "🆘 Апелляция",
        "❓ Помощь",
    }),
)
async def handle_menu_buttons_during_confession(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu())

@router.message(F.text == "💌 Признание")
async def begin(message: Message, state: FSMContext, session: AsyncSession) -> None:
    # This source-only guard covers the first step; send() repeats it for a
    # stale FSM state after a later freeze.
    try:
        await EligibilityService(session).ensure_source_allowed(message.from_user.id, action="отправлять признания")
    except EligibilityError as error:
        await message.answer(str(error))
        return
    await state.set_state(ConfessionState.recipient)
    await message.answer(
        "💌 Анонимное признание\nКому отправить? Введите @username получателя или его числовой Telegram ID.",
        reply_markup=InlineKeyboardBuilder().button(text="❌ Отмена", callback_data="confession:cancel").as_markup()
    )

@router.message(ConfessionState.recipient)
async def recipient(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    valid_username = value.startswith("@") and 3 <= len(value) <= 33
    valid_id = value.isdigit() and 4 <= len(value) <= 20
    if not (valid_username or valid_id):
        await message.answer("⚠️ Введите корректный @username или числовой Telegram ID.")
        return
    await state.update_data(recipient=value)
    await state.set_state(ConfessionState.text)
    await message.answer("✍️ Напишите текст признания (5–1000 символов).")

@router.message(ConfessionState.text)
async def confirmation(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not 5 <= len(text) <= 1000:
        await message.answer("⚠️ Текст должен быть от 5 до 1000 символов.")
        return
    await state.update_data(text=text)
    await state.update_data(submission_key=uuid4().hex)
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Отправить", callback_data="confession:send")
    kb.button(text="❌ Отмена", callback_data="confession:cancel")
    kb.adjust(2)
    await state.set_state(ConfessionState.confirm)
    await message.answer(
        "📩 Проверьте сообщение. Отправитель останется анонимным:\n\n" + escape_html(text),
        reply_markup=kb.as_markup(),
    )

@router.callback_query(F.data == "confession:cancel")
async def cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("❌ Отправка признания отменена.")
    await callback.answer()

@router.callback_query(ConfessionState.confirm, F.data == "confession:send")
async def send(callback: CallbackQuery, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    try:
        await EligibilityService(session).ensure_source_allowed(callback.from_user.id, action="отправлять признания")
    except EligibilityError as error:
        await state.clear()
        await callback.answer(str(error), show_alert=True)
        return
    data = await state.get_data()
    recipient, text = data["recipient"], data["text"]
    try:
        confession = await ConfessionService(
            session,
            settings.daily_secret_salt,
            daily_limit=settings.confession_daily_limit,
            pending_ttl_hours=settings.confession_pending_ttl_hours,
        ).create(callback.from_user.id, recipient, text, submission_key=data.get("submission_key"))
    except ValueError as error:
        await state.clear()
        await callback.message.edit_text(str(error))
        await callback.answer()
        return
    if confession.recipient_id:
        delivered = await NotificationService(callback.bot).safe_send(
            confession.recipient_id, f"💌 Вам анонимное признание:\n\n{escape_html(text)}"
        )
        await callback.message.edit_text(
            "✅ Признание доставлено анонимно."
            if delivered
            else "✅ Признание сохранено, но Telegram временно не подтвердил доставку."
        )
    else:
        link = f"https://t.me/{(await callback.bot.get_me()).username}?start=confession_{confession.id}"
        await callback.message.edit_text(
            f"📎 Получатель ещё не запускал бота. Передайте ему ссылку:\n{link}"
        )
    await state.clear()
    await callback.answer()
