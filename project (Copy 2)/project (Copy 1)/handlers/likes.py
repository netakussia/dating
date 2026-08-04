from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.discovery import DiscoveryRepository
from utils.contacts import telegram_contact

router = Router()


@router.message(F.text == "❤️ Симпатии")
async def likes_history(message: Message, session: AsyncSession) -> None:
    repo = DiscoveryRepository(session)
    likes = await repo.received_likes(message.from_user.id)
    matches = await repo.matches(message.from_user.id)

    received_lines: list[str] = []
    for like in likes[:20]:
        profile, user = await repo.profile_and_user(like.from_user_id)
        label = telegram_contact(
            like.from_user_id,
            user.username if user else None,
            profile.name if profile else "Пользователь",
        )
        if like.is_mutual:
            received_lines.append(f"• ✅ Взаимно: {label}")
        elif like.comment:
            received_lines.append(f"• ❤️ {label}: {like.comment}")
        else:
            received_lines.append(f"• ❤️ {label}")

    match_lines: list[str] = []
    for match in matches[:20]:
        partner_id = match.user2_id if match.user1_id == message.from_user.id else match.user1_id
        profile, user = await repo.profile_and_user(partner_id)
        name = profile.name if profile else "Пользователь"
        match_lines.append(f"• {name} — {telegram_contact(partner_id, user.username if user else None, name)}")

    received_text = "\n".join(received_lines) if received_lines else "Пока нет входящих лайков."
    matches_text = "\n".join(match_lines) if match_lines else "Пока нет взаимных симпатий."
    await message.answer(f"<b>Входящие лайки</b>\n{received_text}\n\n<b>Взаимные симпатии и контакты</b>\n{matches_text}")
