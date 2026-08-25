from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Profile, Report, ReportReason, ReportStatus, User, UserStatus


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None: self.session = session
    async def add(
        self,
        reporter_id: int,
        target_id: int,
        reason: ReportReason,
        *,
        threshold: int = 3,
        evidence_snapshot: dict[str, object] | None = None,
    ) -> tuple[Report, bool, bool]:
        existing = await self.session.scalar(
            select(Report).where(Report.reporter_id == reporter_id, Report.target_user_id == target_id)
        )
        if existing is not None:
            return existing, False, False

        try:
            async with self.session.begin_nested():
                report = Report(
                    reporter_id=reporter_id,
                    target_user_id=target_id,
                    reason=reason,
                    evidence_snapshot=evidence_snapshot,
                )
                self.session.add(report)
                await self.session.flush()

                updated_profile = await self.session.execute(
                    update(Profile)
                    .where(Profile.user_id == target_id)
                    .values(report_count=Profile.report_count + 1)
                    .returning(Profile.user_id, Profile.report_count, Profile.is_visible, Profile.moderation_locked)
                )
                row = updated_profile.one_or_none()
                threshold_reached = False
                if row is not None:
                    new_report_count = int(row.report_count)
                    # Only the transaction that crosses the threshold owns the
                    # suspension and moderation-case side effect.
                    threshold_reached = new_report_count == threshold
                    if threshold_reached:
                        await self.session.execute(
                            update(Profile)
                            .where(
                                Profile.user_id == target_id,
                                Profile.is_visible.is_(True),
                                Profile.moderation_locked.is_(False),
                            )
                            .values(is_visible=False, moderation_locked=True)
                        )
                        await self.session.execute(
                            update(User)
                            .where(User.id == target_id, User.status != UserStatus.SUSPENDED)
                            .values(status=UserStatus.SUSPENDED)
                        )
        except IntegrityError:
            existing = await self.session.scalar(
                select(Report).where(Report.reporter_id == reporter_id, Report.target_user_id == target_id)
            )
            return existing, False, False
        return report, True, threshold_reached
    async def pending(self) -> list[Report]:
        statement = select(Report).where(Report.status == ReportStatus.PENDING).order_by(Report.created_at)
        return list((await self.session.scalars(statement)).all())

    async def get(self, report_id):
        return await self.session.get(Report, report_id)

    async def claim(self, report_id, moderator_id: int) -> Report | None:
        """Claim a report for processing."""
        result = await self.session.execute(
            update(Report)
            .where(
                Report.id == report_id,
                Report.status == ReportStatus.PENDING,
                (Report.assigned_to.is_(None) | (Report.assigned_to == moderator_id)),
            )
            .values(assigned_to=moderator_id, assigned_at=datetime.now(UTC))
            .returning(Report)
        )
        report = result.scalar_one_or_none()
        if report is not None:
            return report
        current = await self.get(report_id)
        if current is None or current.status != ReportStatus.PENDING:
            return None
        if current.assigned_to not in {None, moderator_id}:
            return None
        current.assigned_to = moderator_id
        current.assigned_at = datetime.now(UTC)
        await self.session.flush()
        return current

    async def resolve(self, report_id, status: ReportStatus) -> Report | None:
        result = await self.session.execute(
            update(Report)
            .where(Report.id == report_id, Report.status == ReportStatus.PENDING)
            .values(status=status)
            .returning(Report)
        )
        return result.scalar_one_or_none()
