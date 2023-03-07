import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand

from app.handlers import add_expenses, common_handlers
from config.bot_config import bot, dp, BASE_DIR, ADMIN_ID
from config.middlewares import AccessMiddleware

LOGGER = 'bot.log'


async def set_commands(bot: Bot):
    """Creating a bot menu

    :param bot: an instance of the bot class
    :return:
    """
    commands = [
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/categories', description='Список категорий'),
    ]

    await bot.set_my_commands(commands)


async def main():
    """Bot launch

    :return: None
    """
    logging.basicConfig(filename=f'{str(BASE_DIR)}\\{LOGGER}',
                        format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    logging.info('Starting bot')
    dp.middleware.setup(AccessMiddleware(ADMIN_ID))

    common_handlers(dp)
    add_expenses(dp)

    await set_commands(bot)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
