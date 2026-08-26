from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from models import VerificationStatus
from repositories.trust import TrustRepository
from services.notification_service import InternalNotificationService, NotificationService
from services.profile_service import ProfileService
from services.verification_service import VerificationService
from states.verification import VerificationState
from utils.admin_ui import compact_display_id, user_display_name

router = Router()


def verification_navigation_keyboard(show_retake: bool = False) -> InlineKeyboardMarkup:
    buttons = []
    if show_retake:
        buttons.append([InlineKeyboardButton(text="🔄 Повторить проверку", callback_data="verification:start_upload")])
    buttons.append([
        InlineKeyboardButton(text="👤 Моя анкета", callback_data="promo:my_profile"),
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="verification:home"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "verification:home")
async def verification_home(callback: CallbackQuery) -> None:
    await callback.answer()
    from keyboards.menu import main_menu
    await callback.message.answer("🏠 Главное меню", reply_markup=main_menu())


@router.callback_query(F.data == "verification:start_upload")
async def verification_start_upload(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(VerificationState.waiting_video)
    await callback.answer()
    await callback.message.answer(
        "🛡 Повторная верификация\nОтправьте короткое видеосообщение-кружок для повторной проверки модераторами."
    )


@router.message(F.text == "🛡 Верификация")
async def verification_start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(message.from_user.id)
    if profile is None:
        await message.answer(
            "📝 Для прохождения верификации сначала необходимо создать анкету.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="✨ Создать анкету", callback_data="profile:create")]]
            ),
        )
        return

    status_value = getattr(profile.verification_status, "value", profile.verification_status)
    if status_value == VerificationStatus.VERIFIED.value:
        await message.answer(
            "✅ <b>Вы уже верифицированы</b>\n\n"
            "Ваша анкета имеет подтвержденный статус (зеленая галочка). Повторная проверка сейчас не требуется.",
            reply_markup=verification_navigation_keyboard(show_retake=False),
        )
        return

    if status_value == VerificationStatus.PENDING.value:
        await message.answer(
            "⏳ <b>Ваша заявка уже на рассмотрении</b>\n\n"
            "Модераторы проверяют отправленный видеокружок. Пожалуйста, ожидайте решения.",
            reply_markup=verification_navigation_keyboard(show_retake=False),
        )
        return

    await state.set_state(VerificationState.waiting_video)
    await message.answer(
        "🛡 Верификация\nОтправьте короткое видеосообщение-кружок — модераторы увидят его только для проверки."
    )


@router.message(VerificationState.waiting_video, F.video_note)
async def verification_video(message: Message, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    try:
        request = await VerificationService(session).submit(message.from_user.id, message.video_note.file_id)
    except ValueError as exc:
        # Friendly message for known validation errors (already verified / pending request)
        await state.clear()
        await message.answer(str(exc))
        return

    await state.clear()
    await InternalNotificationService(message.bot, settings).send_moderation_event(
        "Новая verification request",
        user_id=request.user_id,
        username=message.from_user.username,
        reason="verification request",
        case_id=str(request.id),
        target_callback=f"mycase:verify:{request.id}",
        details=f"Verification case: {compact_display_id(request.id)}",
    )
    notifier = NotificationService(message.bot)
    for admin_id in settings.admin_ids:
        await notifier.safe_send(
            admin_id,
            (
                f"🛡 Новая верификация {compact_display_id(request.id)}\n"
                f"Пользователь: {user_display_name(request.user_id)}"
            ),
            dedupe_key=f"verification:{request.id}",
        )
        await TrustRepository(session).log(
            admin_id,
            "verification_notice_sent",
            target_type="verification",
            target_id=str(request.id),
            metadata={"user_id": request.user_id},
        )
    await message.answer(
        "✅ Видеокружок отправлен на проверку. Статус анкеты пока: непроверенный."
    )


@router.message(VerificationState.waiting_video)
async def verification_not_video(message: Message) -> None:
    await message.answer("⚠️ Нужно отправить именно видеосообщение-кружок.")
