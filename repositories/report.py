from sqlalchemy import select
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
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == target_id))
        if profile:
            profile.report_count += 1
            threshold_reached = profile.report_count == threshold
            if profile.report_count >= threshold:
                profile.is_visible = False
                profile.moderation_locked = True
                user = await self.session.get(User, target_id)
                if user:
                    user.status = UserStatus.SUSPENDED
        else:
            threshold_reached = False
        await self.session.flush()
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
