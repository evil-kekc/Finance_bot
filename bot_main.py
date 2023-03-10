import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand

from app.handlers import add_expenses, common_handlers, get_expenses
from config.bot_config import bot, dp, BASE_DIR, ADMIN_ID, LOGGER
from config.middlewares import AccessMiddleware, UpdateLastActiveMiddleware


async def set_commands(bot: Bot):
    """Creating a bot menu

    :param bot: an instance of the bot class
    :return:
    """
    commands = [
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/add_expense', description='Список категорий'),
        BotCommand(command='/cancel', description='Отмена действий'),
        BotCommand(command='/get_all_expenses', description='Сумма всех расходов'),
        BotCommand(command='/get_month_expenses', description='Расходы за месяц'),
        BotCommand(command='/get_week_expenses', description='Расходы за неделю'),
        BotCommand(command='/get_day_expenses', description='Расходы за день'),
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
    dp.middleware.setup(UpdateLastActiveMiddleware())

    common_handlers(dp)
    get_expenses(dp)
    add_expenses(dp)

    await set_commands(bot)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
