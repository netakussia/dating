import hashlib
import re
import uuid
from datetime import UTC, date, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from models import Confession, ConfessionStatus, UserStatus
from repositories.confession import ConfessionRepository
from repositories.user import UserRepository


class ConfessionService:
    def __init__(
        self, session: AsyncSession, salt: str, *, daily_limit: int = 20, pending_ttl_hours: int = 168
    ) -> None:
        self.session, self.salt, self.daily_limit = session, salt, daily_limit
        self.pending_ttl_hours = pending_ttl_hours
    def sender_hash(self, user_id: int) -> str:
        return hashlib.sha256(f"{user_id}:{date.today().isoformat()}:{self.salt}".encode()).hexdigest()
    async def create(
        self, sender_id: int, recipient: str, text: str, *, submission_key: str | None = None
    ) -> Confession:
        """Create a confession record after validating inputs.

        Raises ValueError for invalid input (empty recipient or invalid text length).
        """
        if not (text and 5 <= len(text.strip()) <= 1000):
            raise ValueError("Text length must be between 5 and 1000 characters")
        if not (recipient and recipient.strip()):
            raise ValueError("Recipient must be provided as @username or Telegram ID")

        repo = ConfessionRepository(self.session)
        if submission_key:
            existing = await repo.by_submission_key(submission_key)
            if existing is not None:
                return existing

        normalized = recipient.strip().lstrip("@")
        if normalized.isdigit() and int(normalized) == sender_id:
            raise ValueError("Нельзя отправить признание самому себе.")
        if not normalized.isdigit() and not re.fullmatch(r"[A-Za-z0-9_]{3,32}", normalized):
            raise ValueError("Укажите корректный Telegram username.")
        user = None
        if normalized.isdigit():
            try:
                user = await UserRepository(self.session).get(int(normalized))
            except Exception:
                user = None
        else:
            user = await UserRepository(self.session).by_username(normalized)

        if user is not None and (
            getattr(user, "status", UserStatus.ACTIVE) != UserStatus.ACTIVE
            or not getattr(user, "accepts_confessions", True)
        ):
            # Do not disclose whether a recipient paused messages or was restricted.
            raise ValueError("Сейчас этому пользователю нельзя отправить признание.")

        sender_hash = self.sender_hash(sender_id)
        if not await repo.reserve_daily_send(sender_hash, limit=self.daily_limit):
            raise ValueError("На сегодня лимит анонимных признаний исчерпан. Попробуйте завтра.")

        confession = Confession(
            sender_hash=sender_hash,
            submission_key=submission_key,
            recipient_id=user.id if user else None,
            target_username=None if user else recipient.lstrip("@"),
            text=text.strip(),
            status=ConfessionStatus.DELIVERED if user else ConfessionStatus.PENDING,
            expires_at=None if user else datetime.now(UTC) + timedelta(hours=self.pending_ttl_hours),
        )
        return await repo.add(confession)
    async def claim(self, confession_id: uuid.UUID, recipient_id: int) -> Confession | None:
        confession = await ConfessionRepository(self.session).get_pending(confession_id)
        if confession is None:
            return None

        # A pending confession is delivered through a shareable deep link.
        # It can be claimed either by a matching username or by a matching Telegram ID
        # if the sender used an ID instead of a username.
        recipient = await UserRepository(self.session).get(recipient_id)
        if not recipient:
            return None

        expected_target = (confession.target_username or "").lstrip("@").casefold()
        if not expected_target:
            return None

        # Check if target matches either ID or username
        is_match = False
        if expected_target.isdigit():
            is_match = int(expected_target) == recipient_id
        else:
            actual_username = (recipient.username or "").casefold()
            is_match = actual_username == expected_target

        if not is_match:
            return None

        if (
            getattr(recipient, "status", UserStatus.ACTIVE) != UserStatus.ACTIVE
            or not getattr(recipient, "accepts_confessions", True)
        ):
            return None

        return await ConfessionRepository(self.session).claim_pending(confession_id, recipient_id)
