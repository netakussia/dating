from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.discovery import DiscoveryRepository

router = Router()


@router.message(F.text == "❤️ Симпатии")
async def likes_history(message: Message, session: AsyncSession) -> None:
    repo = DiscoveryRepository(session)
    matches = await repo.matches(message.from_user.id)

    match_lines: list[str] = []
    for match in matches[:20]:
        partner_id = match.user2_id if match.user1_id == message.from_user.id else match.user1_id
        profile, user = await repo.profile_and_user(partner_id)
        name = profile.name if profile else "Пользователь"
        contact = f"@{user.username}" if user and user.username else f"<a href=\"tg://user?id={partner_id}\">{name}</a>"
        match_lines.append(f"• {name} — {contact}")

    matches_text = "\n".join(match_lines) if match_lines else "Пока нет взаимных симпатий."
    await message.answer(f"<b>Взаимные симпатии и контакты</b>\n{matches_text}\n\nВходящие лайки остаются анонимными до взаимного лайка.")
