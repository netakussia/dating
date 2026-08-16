from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from repositories.trust import TrustRepository
from services.notification_service import NotificationService
from services.verification_service import VerificationService
from states.verification import VerificationState
from utils.admin_ui import compact_display_id, user_display_name

router = Router()


@router.message(F.text == "🛡 Верификация")
async def verification_start(message: Message, state: FSMContext) -> None:
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
