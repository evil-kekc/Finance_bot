import logging
from typing import NamedTuple

from aiogram import types
from aiogram.utils.callback_data import CallbackData

from bot_config import BASE_DIR
from databases.db import Database


DATABASE = Database(fr'{BASE_DIR}/databases/bot.db', fr'{BASE_DIR}/databases/create_db.sql')

ALL_CATEGORIES = [_.codename for _ in DATABASE.get_categories()]

call_back_confirm = CallbackData('confirmation_expense', 'answer', 'quantity', 'codename')


class ChoiceExpense(NamedTuple):
    user_id: int
    state: str


def create_confirm_expenses_kb(quantity: float, codename: str):
    """Create confirm expenses_kb

    :param quantity: expense amount
    :param codename: expense codename
    :return:
    """
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)

    button_yes = types.InlineKeyboardButton(text='Да',
                                            callback_data=call_back_confirm.new(answer='Yes',
                                                                                quantity=quantity,
                                                                                codename=codename)
                                            )
    button_no = types.InlineKeyboardButton(text='Нет',
                                           callback_data=call_back_confirm.new(answer='No',
                                                                               quantity=quantity,
                                                                               codename=codename)
                                           )
    keyboard.add(button_yes)
    keyboard.add(button_no)
    return keyboard


def quantity_is_valid(quantity: str):
    """Expenditure check for validity

    :param quantity: expense amount
    :return:
    """
    try:
        quantity = float(quantity)
        return quantity
    except Exception as ex:
        logging.info(repr(ex))
        return
