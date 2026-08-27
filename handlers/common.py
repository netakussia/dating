import uuid

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.menu import MENU_HELP_LABELS, main_menu
from models import User
from services.confession_service import ConfessionService
from services.localization import LocalizationService
from services.notification_service import InternalNotificationService
from states.bug_report import BugReportState
from utils.admin_ui import admin_role_label
from utils.document_links import documents_keyboard
from utils.legal import accept_consent, consent_already_given, ensure_consent_for_new_user
from utils.text import escape_html

router = Router()
localizer = LocalizationService()


async def _send_welcome(message: Message, locale: str = "ru") -> None:
    await send_and_pin_alpha_notice(message, locale)
    await message.answer(
        LocalizationService().get("welcome", locale),
        reply_markup=main_menu(locale),
    )


async def send_and_pin_alpha_notice(message: Message, locale: str = "ru") -> None:
    """Send alpha notice and attempt to pin it quietly in private chat."""
    try:
        notice_msg = await message.answer(localizer.get("alpha_notice", locale))
        await notice_msg.pin(disable_notification=True)
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "legal:accept")
async def legal_accept(callback: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str = "ru") -> None:
    await accept_consent(callback, state)
    await _send_welcome(callback.message, locale)


async def _text_start(message: Message, state: FSMContext, session: AsyncSession, settings, locale: str = "ru") -> None:
    await start(message, state, session, settings, locale)


@router.message(F.text.casefold() == "start")
async def text_start(message: Message, state: FSMContext, session: AsyncSession, settings, locale: str = "ru") -> None:
    await _text_start(message, state, session, settings, locale)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, session: AsyncSession, settings, locale: str = "ru") -> None:
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

    if not await ensure_consent_for_new_user(state, session, message.from_user.id, message, locale):
        return

    consent = bool((await state.get_data()).get("legal_consent", False))
    await state.clear()
    if consent:
        await state.update_data(legal_consent=True)

    await _send_welcome(message, locale)


@router.message(F.text.in_({"Продолжить", "✅ Продолжить"}))
async def text_continue(message: Message, state: FSMContext, session: AsyncSession, locale: str = "ru") -> None:
    if not await consent_already_given(state):
        await message.answer(
            LocalizationService().get("legal_notice", locale),
            reply_markup=documents_keyboard(
                "terms",
                "privacy",
                "community",
                "safety",
                "moderation",
                "alpha",
                include_continue=True,
                locale=locale,
            ),
        )
        return
    await _send_welcome(message, locale)


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
@router.message(lambda m: m.text in MENU_HELP_LABELS or m.text in {"⚙️ Настройки", "Настройки"})
async def help_(message: Message, settings, session: AsyncSession, locale: str = "ru") -> None:
    admin_ids = sorted(settings.admin_ids)
    support_lines = []
    for admin_id in admin_ids:
        user = await session.get(User, admin_id)
        username = user.username if user and user.username else None
        label = admin_role_label(admin_id, username=username, owner_admin_id=settings.owner_admin_id)
        support_lines.append(f'<a href="tg://user?id={admin_id}">{label}</a>')
    localizer = LocalizationService()
    support = "\n".join(support_lines) if support_lines else localizer.get("help_support_unconfigured", locale)
    markup = documents_keyboard(
        "terms",
        "privacy",
        "community",
        "safety",
        "moderation",
        "alpha",
        locale=locale,
    )
    markup.inline_keyboard.append(
        [InlineKeyboardButton(text=localizer.get("menu_profile", locale), callback_data="promo:my_profile")]
    )
    markup.inline_keyboard.append(
        [InlineKeyboardButton(text=localizer.get("help_report_problem", locale), callback_data="bug_report:start")]
    )
    await message.answer(localizer.get("help_text", locale), reply_markup=markup)
    await message.answer(
        f"{localizer.get('help_support_prompt', locale)}\n{support}",
    )
