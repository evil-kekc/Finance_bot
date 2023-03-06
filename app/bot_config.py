import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config_reader import load_config

BASE_DIR = Path(os.path.abspath(__file__)).parent.parent

config = load_config(f'{BASE_DIR}\\config\\bot_config.ini')

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(bot, storage=MemoryStorage())
