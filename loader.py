import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from . import proxy
from data import config


database = sqlite3.connect("bot.sqlite")
cursor = database.cursor()

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, protect_content=False)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
proxy = proxy.GPTProxy(config.API_TOKEN)
