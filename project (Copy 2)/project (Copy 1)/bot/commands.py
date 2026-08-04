from aiogram import Bot
from aiogram.types import BotCommand
async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands([BotCommand(command="start", description="Открыть бота"), BotCommand(command="help", description="Помощь"), BotCommand(command="admin", description="Админ-панель")])
