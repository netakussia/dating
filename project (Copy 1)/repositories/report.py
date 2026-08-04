from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Profile, Report, ReportReason, ReportStatus

class ReportRepository:
    def __init__(self, session: AsyncSession) -> None: self.session = session
    async def add(self, reporter_id: int, target_id: int, reason: ReportReason) -> Report:
        report = Report(reporter_id=reporter_id, target_user_id=target_id, reason=reason)
        self.session.add(report)
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == target_id))
        if profile:
            profile.report_count += 1
            if profile.report_count >= 3: profile.is_visible = False
        await self.session.flush(); return report
    async def pending(self) -> list[Report]:
        return list((await self.session.scalars(select(Report).where(Report.status == ReportStatus.PENDING).order_by(Report.created_at))).all())

    async def get(self, report_id):
        return await self.session.get(Report, report_id)

    async def resolve(self, report_id, status: ReportStatus) -> Report | None:
        report = await self.get(report_id)
        if report and report.status == ReportStatus.PENDING:
            report.status = status
            await self.session.flush()
        return report
