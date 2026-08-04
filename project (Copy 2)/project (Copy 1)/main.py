import asyncio
import logging
import sys

from pydantic import ValidationError
from redis.asyncio import Redis
from bot.commands import set_commands
from bot.factory import create_dispatcher
from config import get_settings
from database.base import Base
from database.connection import make_session_factory
from sqlalchemy.ext.asyncio import create_async_engine
import models  # noqa: F401

async def run() -> None:
    settings = get_settings(); logging.basicConfig(level=settings.log_level)
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
    factory = make_session_factory(settings); redis = Redis.from_url(settings.redis_url)
    bot, dp = create_dispatcher(settings, factory, redis)
    await set_commands(bot)
    try: await dp.start_polling(bot)
    finally: await redis.aclose(); await engine.dispose(); await bot.session.close()
if __name__ == "__main__":
    try:
        asyncio.run(run())
    except ValidationError as error:
        print(
            "\nОШИБКА НАСТРОЙКИ: заполните файл .env рядом с docker-compose.yml.\n"
            "Обязательные строки: BOT_TOKEN=... и DAILY_SECRET_SALT=...\n"
            "Возьмите шаблон из .env.example. Текущая ошибка:\n"
            f"{error}\n",
            file=sys.stderr,
        )
        raise SystemExit(2) from error
