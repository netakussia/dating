import hashlib
import uuid
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from models import Confession, ConfessionStatus
from repositories.confession import ConfessionRepository
from repositories.user import UserRepository

class ConfessionService:
    def __init__(self, session: AsyncSession, salt: str) -> None: self.session, self.salt = session, salt
    def sender_hash(self, user_id: int) -> str:
        return hashlib.sha256(f"{user_id}:{date.today().isoformat()}:{self.salt}".encode()).hexdigest()
    async def create(self, sender_id: int, recipient: str, text: str) -> Confession:
        """Create a confession record after validating inputs.

        Raises ValueError for invalid input (empty recipient or invalid text length).
        """
        if not (text and 5 <= len(text.strip()) <= 1000):
            raise ValueError("Text length must be between 5 and 1000 characters")
        if not (recipient and recipient.strip()):
            raise ValueError("Recipient must be provided as @username or Telegram ID")

        normalized = recipient.strip().lstrip("@")
        user = None
        if normalized.isdigit():
            try:
                user = await UserRepository(self.session).get(int(normalized))
            except Exception:
                user = None
        else:
            user = await UserRepository(self.session).by_username(normalized)

        confession = Confession(
            sender_hash=self.sender_hash(sender_id),
            recipient_id=user.id if user else None,
            target_username=None if user else recipient.lstrip("@"),
            text=text.strip(),
            status=ConfessionStatus.DELIVERED if user else ConfessionStatus.PENDING,
        )
        return await ConfessionRepository(self.session).add(confession)
    async def claim(self, confession_id: uuid.UUID, recipient_id: int) -> Confession | None:
        confession = await ConfessionRepository(self.session).get_pending(confession_id)
        if confession:
            confession.recipient_id, confession.status = recipient_id, ConfessionStatus.DELIVERED
            await self.session.flush()
        return confession
