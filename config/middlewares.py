from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from handlers.common import DATABASE


class AccessMiddleware(BaseMiddleware):
    """Authentication - skip messages from only one Telegram account"""

    def __init__(self, access_id: int):
        self.access_id = access_id
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if int(message.from_user.id) != int(self.access_id):
            await message.answer("К сожалению, у Вас нет доступа к боту. Обратитесь к администратору @evil_kekc")
            raise CancelHandler()
        else:
            DATABASE.add_user(user_id=self.access_id, is_admin=True)


class UpdateLastActiveMiddleware(BaseMiddleware):
    """Update last user activity"""
    def __init__(self):
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        DATABASE.update_last_active(user_id=message.from_user.id)
