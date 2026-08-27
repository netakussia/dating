import uuid

from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    AdminLog,
    ModerationCase,
    ModerationCaseStatus,
    ModerationCaseType,
    PhotoModeration,
    Report,
    ReportStatus,
    TrustScoreEvent,
    User,
    VerificationDecision,
    VerificationRequest,
)


class TrustRepository:
    """Persistence primitives for trust services; policy stays in services/."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def active_verification_for_user(self, user_id: int) -> VerificationRequest | None:
        return await self.session.scalar(
            select(VerificationRequest)
            .where(
                VerificationRequest.user_id == user_id,
                VerificationRequest.status == VerificationDecision.PENDING,
            )
            .order_by(VerificationRequest.created_at.desc())
        )

    async def open_verification(self, user_id: int, video_file_id: str) -> tuple[VerificationRequest, bool]:
        """
        Open a verification request for a user. Returns (request, created) where created
        is True when a new request was created, or False when an existing pending request
        was found and returned.

        This method is defensive: callers may run it under concurrent transactions and
        the DB or elsewhere may also enforce uniqueness. If insertion fails due to a
        race, the method attempts to return the existing pending request.
        """
        active = await self.active_verification_for_user(user_id)
        if active is not None:
            return active, False
        request = VerificationRequest(user_id=user_id, video_file_id=video_file_id)
        try:
            nested = getattr(self.session, "begin_nested", None)
            if nested is None:
                self.session.add(request)
                await self.session.flush()
            else:
                async with nested():
                    self.session.add(request)
                    await self.session.flush()
        except IntegrityError:
            # The savepoint keeps the outer transaction usable after a race.
            existing = await self.active_verification_for_user(user_id)
            if existing:
                return existing, False
            raise
        return request, True

    async def verification(self, request_id: uuid.UUID) -> VerificationRequest | None:
        return await self.session.get(VerificationRequest, request_id)

    async def pending_verifications(self) -> list[VerificationRequest]:
        query = select(VerificationRequest).where(VerificationRequest.status == VerificationDecision.PENDING)
        return list((await self.session.scalars(query.order_by(VerificationRequest.created_at))).all())

    async def open_case(
        self, user_id: int, case_type: ModerationCaseType, *, source_id: str | None = None, details: str | None = None
    ) -> tuple[ModerationCase, bool]:
        query = select(ModerationCase).where(
            ModerationCase.user_id == user_id,
            ModerationCase.case_type == case_type,
            ModerationCase.status.in_((ModerationCaseStatus.PENDING, ModerationCaseStatus.IN_PROGRESS)),
        )
        if source_id is not None:
            query = query.where(ModerationCase.source_id == source_id)
        else:
            query = query.where(ModerationCase.source_id.is_(None))
        existing = await self.session.scalar(query)
        if existing:
            if details is not None and existing.details != details:
                existing.details = details
                await self.session.flush()
            return existing, False
        case = ModerationCase(user_id=user_id, case_type=case_type, source_id=source_id, details=details)
        try:
            nested = getattr(self.session, "begin_nested", None)
            if nested is None:
                self.session.add(case)
                await self.session.flush()
            else:
                async with nested():
                    self.session.add(case)
                    await self.session.flush()
        except IntegrityError:
            existing = await self.session.scalar(query)
            if existing:
                return existing, False
            raise
        return case, True

    async def case(self, case_id: uuid.UUID) -> ModerationCase | None:
        return await self.session.get(ModerationCase, case_id)

    async def pending_cases(self, case_type: ModerationCaseType | None = None) -> list[ModerationCase]:
        query = select(ModerationCase).where(ModerationCase.status == ModerationCaseStatus.PENDING)
        if case_type:
            query = query.where(ModerationCase.case_type == case_type)
        return list((await self.session.scalars(query.order_by(ModerationCase.created_at))).all())

    async def pending_cases_for_user(self, user_id: int) -> list[ModerationCase]:
        return list(
            (
                await self.session.scalars(
                    select(ModerationCase)
                    .where(
                        ModerationCase.user_id == user_id,
                        ModerationCase.status == ModerationCaseStatus.PENDING,
                    )
                    .order_by(ModerationCase.created_at)
                )
            ).all()
        )

    async def close_photo_cases(self, user_id: int, *, source_id: str | None = None) -> int:
        statement = (
            update(ModerationCase)
            .where(
                ModerationCase.user_id == user_id,
                ModerationCase.case_type.in_(
                    (ModerationCaseType.NSFW, ModerationCaseType.NO_FACE, ModerationCaseType.PHOTO_RETAKE)
                ),
                ModerationCase.status.in_((ModerationCaseStatus.PENDING, ModerationCaseStatus.IN_PROGRESS)),
            )
            .values(status=ModerationCaseStatus.RESOLVED)
        )
        if source_id is not None:
            statement = statement.where(ModerationCase.source_id == source_id)
        result = await self.session.execute(statement)
        return int(getattr(result, "rowcount", 0) or 0)

    async def photo_by_hash(self, content_hash: str) -> PhotoModeration | None:
        return await self.session.scalar(
            select(PhotoModeration)
            .where(PhotoModeration.content_hash == content_hash)
            .order_by(PhotoModeration.created_at)
        )

    async def photo_for_case(self, user_id: int, source_id: str | None) -> PhotoModeration | None:
        query = select(PhotoModeration).where(PhotoModeration.user_id == user_id)
        if source_id:
            query = query.where(
                (PhotoModeration.content_hash == source_id) | (PhotoModeration.photo_file_id == source_id)
            )
        return await self.session.scalar(query.order_by(PhotoModeration.created_at.desc()))

    async def record_photo(
        self,
        user_id: int,
        photo_file_id: str,
        provider: str,
        nsfw_score: float,
        face_detected: bool,
        content_hash: str | None = None,
    ) -> PhotoModeration:
        if content_hash:
            existing = await self.session.scalar(
                select(PhotoModeration).where(
                    PhotoModeration.user_id == user_id, PhotoModeration.content_hash == content_hash
                )
            )
            if existing:
                return existing
        item = PhotoModeration(
            user_id=user_id,
            photo_file_id=photo_file_id,
            content_hash=content_hash,
            provider=provider,
            nsfw_score=nsfw_score,
            face_detected=face_detected,
        )
        self.session.add(item)
        await self.session.flush()
        return item

    async def add_score_event(
        self, user_id: int, delta: int, reason: str, reference_type: str | None, reference_id: str | None
    ) -> TrustScoreEvent:
        event = TrustScoreEvent(
            user_id=user_id,
            delta=delta,
            reason=reason,
            reference_type=reference_type,
            reference_id=reference_id,
        )
        self.session.add(event)
        await self.session.flush()
        return event

    async def log(
        self,
        admin_id: int,
        action: str,
        *,
        target_type: str | None = None,
        target_id: str | None = None,
        target_user_id: int | None = None,
        details: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> AdminLog:
        item = AdminLog(
            admin_id=admin_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            target_user_id=target_user_id,
            details=details,
            metadata_json=metadata or {},
        )
        self.session.add(item)
        await self.session.flush()
        return item

    async def history(self, limit: int = 30) -> list[AdminLog]:
        return list(
            (await self.session.scalars(select(AdminLog).order_by(AdminLog.created_at.desc()).limit(limit))).all()
        )

    async def stats(self) -> dict[str, float | int]:
        verified = await self.session.scalar(
            select(func.count(VerificationRequest.id)).where(
                VerificationRequest.status == VerificationDecision.APPROVED
            )
        )
        reports = await self.session.scalar(select(func.count()).select_from(Report))
        false_reports = await self.session.scalar(
            select(func.count()).select_from(Report).where(Report.status == ReportStatus.DISMISSED)
        )
        confirmed_fakes = await self.session.scalar(
            select(func.count()).select_from(TrustScoreEvent).where(TrustScoreEvent.reason == "confirmed_fake")
        )
        average = await self.session.scalar(select(func.avg(User.trust_score)))
        return {
            "verified": int(verified or 0),
            "reports": int(reports or 0),
            "false_reports": int(false_reports or 0),
            "confirmed_fakes": int(confirmed_fakes or 0),
            "average_trust_score": round(float(average or 0), 2),
        }
