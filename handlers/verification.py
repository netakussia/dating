from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from services.notification_service import NotificationService
from services.verification_service import VerificationService
from states.verification import VerificationState

router = Router()


@router.message(F.text == "🛡 Верификация")
async def verification_start(message: Message, state: FSMContext) -> None:
    await state.set_state(VerificationState.waiting_video)
    await message.answer("Отправьте короткое видеосообщение-кружок. Его увидят только модераторы.")


@router.message(VerificationState.waiting_video, F.video_note)
async def verification_video(message: Message, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    request = await VerificationService(session).submit(message.from_user.id, message.video_note.file_id)
    await state.clear()
    notifier = NotificationService(message.bot)
    for admin_id in settings.admin_ids:
        await notifier.safe_send(
            admin_id, f"🛡 Новая верификация #{request.id}; пользователь <code>{request.user_id}</code>"
        )
    await message.answer("✅ Кружок отправлен на проверку. Статус анкеты пока: непроверенный.")


@router.message(VerificationState.waiting_video)
async def verification_not_video(message: Message) -> None:
    await message.answer("Нужно отправить именно видеосообщение-кружок.")
