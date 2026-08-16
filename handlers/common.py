import uuid

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.menu import main_menu
from models import User
from services.confession_service import ConfessionService
from utils.admin_ui import admin_role_label
from utils.document_links import documents_keyboard
from utils.legal import accept_consent, ensure_consent_for_new_user

router = Router()


@router.callback_query(F.data == "legal:accept")
async def legal_accept(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await accept_consent(callback, state)
    await callback.message.answer(
        "👋 Добро пожаловать!\nСоздайте анкету через «👤 Моя анкета» или начните знакомства через «💘 Знакомства».",
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
                await message.answer(f"💌 Вам анонимное признание:\n\n{confession.text}")
        except ValueError:
            pass

    if not await ensure_consent_for_new_user(state, session, message.from_user.id, message):
        return

    consent = bool((await state.get_data()).get("legal_consent", False))
    await state.clear()
    if consent:
        await state.update_data(legal_consent=True)
    await message.answer(
        "👋 Добро пожаловать!\nСоздайте анкету через «👤 Моя анкета» или начните знакомства через «💘 Знакомства».",
        reply_markup=main_menu(),
    )


@router.message(Command("help"))
@router.message(lambda m: m.text == "❓ Помощь")
async def help_(message: Message, settings, session: AsyncSession) -> None:
    admin_ids = sorted(settings.admin_ids)
    support_lines = []
    for index, admin_id in enumerate(admin_ids):
        user = await session.get(User, admin_id)
        username = user.username if user and user.username else None
        label = admin_role_label(admin_id, username=username, owner_admin_id=admin_ids[0] if admin_ids else None)
        support_lines.append(f'<a href="tg://user?id={admin_id}">{label}</a>')
    support = "\n".join(support_lines) if support_lines else "Служба поддержки не настроена."
    await message.answer(
        "❓ <b>Помощь</b>\n"
        "Переходите в «👤 Моя анкета» для создания или редактирования анкеты, \n"
        "а затем откройте «💘 Знакомства» для поиска.\n\n"
        "Признания отправляются анонимно.\n\n"
        "📚 <b>Документы MeAnima</b>",
        reply_markup=documents_keyboard(
            "terms",
            "privacy",
            "community",
            "safety",
            "moderation",
            "alpha",
        ),
    )
    await message.answer(
        f"Если нужна помощь, напишите одному из администраторов:\n{support}",
    )
