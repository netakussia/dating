import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.token import TokenValidationError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config import Settings
from handlers import routers
from middlewares.db import DbSessionMiddleware
from middlewares.i18n import FSMI18nMiddleware
from middlewares.profile_required import ProfileRequiredMiddleware
from middlewares.rate_limit import RateLimitMiddleware
from middlewares.user import UserSyncMiddleware

logger = logging.getLogger(__name__)


def create_dispatcher(
    settings: Settings, factory: async_sessionmaker[AsyncSession], redis: Redis
) -> tuple[Bot | None, Dispatcher]:
    """
    Create and return (bot, dispatcher). If BOT_TOKEN is invalid, return (None, dispatcher)
    and log a warning — caller should handle offline mode.
    """
    try:
        bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    except TokenValidationError:
        logger.warning("BOT_TOKEN appears invalid — running in offline mode (no Telegram connection).")
        bot = None
    # The same Redis connection backs FSM expiry and notification deduplication.
    dp = Dispatcher(
        storage=RedisStorage(
            redis=redis,
            state_ttl=settings.fsm_state_ttl_seconds,
            data_ttl=settings.fsm_state_ttl_seconds,
        )
    )
    if bot is not None:
        bot.notification_redis = redis
    dp.update.outer_middleware(DbSessionMiddleware(factory))
    dp.update.outer_middleware(UserSyncMiddleware())
    dp.update.outer_middleware(FSMI18nMiddleware())
    dp.update.outer_middleware(ProfileRequiredMiddleware())
    dp.update.outer_middleware(RateLimitMiddleware(redis))
    for router in routers:
        dp.include_router(router)
    dp["settings"] = settings
    return bot, dp
