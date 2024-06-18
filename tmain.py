import logging
import asyncio
from data import config
from aiogram import executor
from aiogram import types
import handlers
from loader import bot, dp
from utils import mess

logging.basicConfig(level=logging.INFO)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
    ])


async def on_startup(dispatcher):
    await bot.send_message(config.ADMIN_ID, mess.BOT_STARTED)
    await set_default_commands(dispatcher)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
