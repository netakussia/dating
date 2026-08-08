from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Profile, Report, ReportReason, ReportStatus, User, UserStatus


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None: self.session = session
    async def add(
        self, reporter_id: int, target_id: int, reason: ReportReason, *, threshold: int = 3
    ) -> tuple[Report, bool, bool]:
        existing = await self.session.scalar(
            select(Report).where(Report.reporter_id == reporter_id, Report.target_user_id == target_id)
        )
        if existing is not None:
            return existing, False, False

        report = Report(reporter_id=reporter_id, target_user_id=target_id, reason=reason)
        self.session.add(report)

        try:
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
                threshold_reached = new_report_count >= threshold
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
            await self.session.flush()
        except IntegrityError:
            await self.session.rollback()
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

    async def resolve(self, report_id, status: ReportStatus) -> Report | None:
        report = await self.get(report_id)
        if report and report.status == ReportStatus.PENDING:
            report.status = status
            await self.session.flush()
        return report
