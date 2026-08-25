from repositories.appeal import AppealRepository as AppealRepository
from repositories.confession import ConfessionRepository as ConfessionRepository
from repositories.discovery import DiscoveryRepository as DiscoveryRepository
from repositories.like import LikeRepository as LikeRepository
from repositories.match import MatchRepository as MatchRepository
from repositories.matching_stats import MatchingStatsRepository as MatchingStatsRepository
from repositories.profile import ProfileRepository as ProfileRepository
from repositories.recommendation import RecommendationRepository as RecommendationRepository
from repositories.report import ReportRepository as ReportRepository
from repositories.user import UserRepository as UserRepository

__all__ = (
    "AppealRepository",
    "ConfessionRepository",
    "DiscoveryRepository",
    "LikeRepository",
    "MatchRepository",
    "MatchingStatsRepository",
    "ProfileRepository",
    "RecommendationRepository",
    "ReportRepository",
    "UserRepository",
)
