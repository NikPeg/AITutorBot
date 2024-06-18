import logging
import asyncio
from data import config
from aiogram import executor
from aiogram import types

from loader import bot, dp
from utils import mess

logging.basicConfig(level=logging.INFO)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
    ])


FEEDBACK_PERIOD = 24 * 60 * 60


async def start_feed_back():
    while True:
        await asyncio.sleep(FEEDBACK_PERIOD)


async def on_startup(dispatcher):
    await bot.send_message(config.ADMIN_ID, mess.BOT_STARTED)
    await set_default_commands(dispatcher)
    asyncio.create_task(start_feed_back())


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
