from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton

from bot_config import BASE_DIR
from databases.db import Database

DATABASE = Database(fr'{BASE_DIR}/databases/bot.db', fr'{BASE_DIR}/databases/create_db.sql')


async def cmd_start(message: types.Message, state: FSMContext):
    """Handling the start command

    :param message: message object
    :param state: state object
    :return:
    """
    await state.finish()
    await message.answer('Привет, я бот, который поможет тебе вести финансы', reply_markup=types.ReplyKeyboardRemove())


async def get_list_of_expenses(message: types.Message):
    """Displaying information about expense categories

    :param message: message object
    :return:
    """
    all_categories = DATABASE.get_categories()
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    for category in all_categories:
        button = InlineKeyboardButton(text=category.name, callback_data=f'{category.codename}')
        keyboard.add(button)

    await message.answer('Доступны следующие категории расходов: ', reply_markup=keyboard)


async def cmd_cancel(message: types.Message, state: FSMContext):
    """Handling the cancel command

    :param message: message object
    :param state: state object
    :return:
    """
    await state.finish()
    await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    """Handler registration function

    :param dp: Dispatcher object
    :return:
    """
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_message_handler(get_list_of_expenses, commands='categories', state='*')
    dp.register_message_handler(cmd_start, Text(equals='отмена', ignore_case=True), state='*')