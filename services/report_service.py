from sqlalchemy.ext.asyncio import AsyncSession

from models import ModerationCaseType, ModerationStatus, ReportReason, ReportStatus
from repositories.discovery import DiscoveryRepository
from repositories.profile import ProfileRepository
from repositories.report import ReportRepository
from repositories.trust import TrustRepository
from services.eligibility import EligibilityError, EligibilityService
from services.trust_score_service import TrustScoreService


class ReportService:
    def __init__(self, session: AsyncSession, *, threshold: int) -> None:
        self.session = session
        self.threshold = threshold

    async def submit(self, reporter_id: int, target_id: int, reason: ReportReason):
        try:
            await EligibilityService(self.session).ensure_action_allowed(reporter_id, target_id, action="пожаловаться")
        except EligibilityError as error:
            raise ValueError(str(error)) from error

        target_profile = await ProfileRepository(self.session).by_user_id(target_id)
        evidence_snapshot = self._evidence_snapshot(target_profile)
        report, created, threshold_reached = await ReportRepository(self.session).add(
            reporter_id,
            target_id,
            reason,
            threshold=self.threshold,
            evidence_snapshot=evidence_snapshot,
        )
        await DiscoveryRepository(self.session).block(reporter_id, target_id)
        if created:
            await TrustScoreService(self.session).change(
                target_id, -10, "report_received", reference_type="report", reference_id=str(report.id)
            )
        if threshold_reached:
            profile = await ProfileRepository(self.session).by_user_id(target_id)
            if profile:
                profile.moderation_status = ModerationStatus.UNDER_REVIEW
            await TrustRepository(self.session).open_case(
                target_id,
                ModerationCaseType.REPORT_THRESHOLD,
                source_id=str(report.id),
                details=f"Reached {self.threshold} unique reports",
            )
        return report, created, threshold_reached

    @staticmethod
    def _evidence_snapshot(profile) -> dict[str, object]:
        """Capture report evidence before later profile edits or deletion."""
        if profile is None:
            return {}
        return {
            "name": profile.name,
            "age": profile.age,
            "district": profile.district,
            "institution": profile.institution,
            "bio": profile.bio,
            "interests": list(profile.interests or []),
            "photo_file_ids": list(profile.photo_file_ids or []),
            "main_photo_file_id": profile.main_photo_file_id,
        }

    async def dismiss(self, report_id, admin_id: int):
        repo = ReportRepository(self.session)
        report = await repo.resolve(report_id, ReportStatus.DISMISSED)
        if report:
            await TrustScoreService(self.session).change(
                report.reporter_id, -5, "false_report", reference_type="report", reference_id=str(report.id)
            )
            await TrustRepository(self.session).log(
                admin_id, "report_dismissed", target_type="report", target_id=str(report.id)
            )
        return report

    async def confirm_fake(self, report_id, admin_id: int):
        repo = ReportRepository(self.session)
        report = await repo.resolve(report_id, ReportStatus.APPROVED)
        if report:
            await TrustScoreService(self.session).change(
                report.target_user_id, -40, "confirmed_fake", reference_type="report", reference_id=str(report.id)
            )
            await TrustRepository(self.session).log(
                admin_id, "report_confirmed_fake", target_type="report", target_id=str(report.id)
            )
        return report
