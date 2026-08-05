from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config import Settings
from handlers import routers
from middlewares.db import DbSessionMiddleware
from middlewares.profile_required import ProfileRequiredMiddleware
from middlewares.rate_limit import RateLimitMiddleware
from middlewares.user import UserSyncMiddleware


def create_dispatcher(
    settings: Settings, factory: async_sessionmaker[AsyncSession], redis: Redis
) -> tuple[Bot, Dispatcher]:
    bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.update.outer_middleware(DbSessionMiddleware(factory))
    dp.update.outer_middleware(UserSyncMiddleware())
    dp.update.outer_middleware(ProfileRequiredMiddleware())
    dp.update.outer_middleware(RateLimitMiddleware(redis))
    for router in routers:
        dp.include_router(router)
    dp["settings"] = settings
    return bot, dp
