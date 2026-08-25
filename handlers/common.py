import uuid

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.menu import main_menu
from models import User
from services.confession_service import ConfessionService
from services.notification_service import InternalNotificationService
from states.bug_report import BugReportState
from utils.admin_ui import admin_role_label
from utils.document_links import documents_keyboard
from utils.legal import accept_consent, ensure_consent_for_new_user
from utils.text import escape_html

ALPHA_NOTICE_TEXT = (
    "🚀 <b>Внимание: Альфа-версия MeAnima</b>\n\n"
    "Бот находится в режиме активного тестирования. "
    "Если вы обнаружите баг или ошибку, нажмите «❓ Помощь» → «🐛 Сообщить о проблеме»."
)

router = Router()


async def send_and_pin_alpha_notice(message: Message) -> None:
    """Send alpha notice and attempt to pin it quietly in private chat."""
    try:
        notice_msg = await message.answer(ALPHA_NOTICE_TEXT)
        await notice_msg.pin(disable_notification=True)
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "legal:accept")
async def legal_accept(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await accept_consent(callback, state)
    await send_and_pin_alpha_notice(callback.message)
    await callback.message.answer(
        "👋 Добро пожаловать в MeAnima!\n\n"
        "Заполните анкету в «👤 Моя анкета», чтобы найти близких по духу людей, "
        "или перейдите в «💘 Знакомства» для просмотра профилей.",
        reply_markup=main_menu(),
    )


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, session: AsyncSession, settings) -> None:
    args = message.text.split(maxsplit=1)
    if len(args) == 2 and args[1].startswith("confession_"):
        try:
            confession = await ConfessionService(session, settings.daily_secret_salt).claim(
                uuid.UUID(args[1].removeprefix("confession_")), message.from_user.id
            )
            if confession:
                await message.answer(f"💌 Вам анонимное признание:\n\n{escape_html(confession.text)}")
        except ValueError:
            pass

    if not await ensure_consent_for_new_user(state, session, message.from_user.id, message):
        return

    consent = bool((await state.get_data()).get("legal_consent", False))
    await state.clear()
    if consent:
        await state.update_data(legal_consent=True)

    await send_and_pin_alpha_notice(message)
    await message.answer(
        "👋 Добро пожаловать в MeAnima!\n\n"
        "Заполните анкету в «👤 Моя анкета», чтобы найти близких по духу людей, "
        "или перейдите в «💘 Знакомства» для просмотра профилей.",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "bug_report:start")
async def bug_report_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BugReportState.waiting_description)
    await callback.answer()
    await callback.message.answer(
        "🐛 Опишите проблему коротко и по сути. Можно также отправить скриншот вместе с описанием."
    )


@router.message(BugReportState.waiting_description)
async def bug_report_submit(message: Message, state: FSMContext, settings) -> None:
    text = (message.text or message.caption or "").strip()
    if not text:
        await message.answer("⚠️ Опишите проблему одним сообщением, чтобы мы смогли разобраться.")
        return
    context = "\n".join(
        [
            f"chat_type={message.chat.type}",
            f"chat_id={message.chat.id}",
            f"message_id={message.message_id}",
            f"location={message.location is not None}",
        ]
    )
    await InternalNotificationService(message.bot, settings).send_bug_report(
        message.from_user.id,
        username=message.from_user.username,
        description=text,
        context=context,
    )
    await state.clear()
    await message.answer("✅ Сообщение о проблеме отправлено. Спасибо — мы посмотрим и исправим.")


@router.message(Command("help"))
@router.message(lambda m: m.text in {"❓ Помощь", "⚙️ Настройки", "Настройки"})
async def help_(message: Message, settings, session: AsyncSession) -> None:
    admin_ids = sorted(settings.admin_ids)
    support_lines = []
    for admin_id in admin_ids:
        user = await session.get(User, admin_id)
        username = user.username if user and user.username else None
        label = admin_role_label(admin_id, username=username, owner_admin_id=admin_ids[0] if admin_ids else None)
        support_lines.append(f'<a href="tg://user?id={admin_id}">{label}</a>')
    support = "\n".join(support_lines) if support_lines else "Служба поддержки не настроена."
    markup = documents_keyboard(
        "terms",
        "privacy",
        "community",
        "safety",
        "moderation",
        "alpha",
    )
    markup.inline_keyboard.append(
        [InlineKeyboardButton(text="� Моя анкета", callback_data="promo:my_profile")]
    )
    markup.inline_keyboard.append(
        [InlineKeyboardButton(text="�🐛 Сообщить о проблеме", callback_data="bug_report:start")]
    )
    await message.answer(
        "❓ <b>Помощь</b>\n"
        "Переходите в «👤 Моя анкета» для создания или редактирования анкеты, \n"
        "а затем откройте «💘 Знакомства» для поиска.\n\n"
        "Признания отправляются анонимно.\n\n"
        "📚 <b>Документы MeAnima</b>",
        reply_markup=markup,
    )
    await message.answer(
        f"Если нужна помощь, напишите одному из администраторов:\n{support}",
    )
