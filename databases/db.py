import logging
import sqlite3 as sq
from collections import namedtuple
from sqlite3 import OperationalError
from typing import NamedTuple

from app.bot_config import BASE_DIR

LOGGER = 'databases.log'
logging.basicConfig(filename=f'{str(BASE_DIR)}\\{LOGGER}',
                    format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


class Category(NamedTuple):
    """Processing the output of the expense name and its codename"""
    name: str
    codename: str


class Database:
    def __init__(self, db_file: str, sql_script_file: str):
        self.connection = sq.connect(db_file)
        self.cursor = self.connection.cursor()
        self.sql_script = sql_script_file
        self._create_db()

    def _create_db(self) -> None:
        """Create a tables

        :return: None
        """
        with open(self.sql_script, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()

        try:
            with self.connection:
                self.cursor.executescript(sql_script)
            logging.info('Database users connected')
        except OperationalError:
            logging.info('Database users already exists')

    def get_categories(self):
        """Getting all categories from the database

        :return: category generator object
        """
        try:

            with self.connection:
                result = self.cursor.execute("SELECT name, codename FROM categories")
                for category in result:
                    result = Category(name=category[0].title(), codename=category[1])
                    yield result
        except Exception as ex:
            logging.error(repr(ex))

    # def add_user(self, user_id):
    #     """Добавление пользователя в базу данных
    #
    #     :param user_id: id пользователя
    #     :return:
    #     """
    #     try:
    #         with self.connection:
    #             self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
    #             self.connection.commit()
    #             return {
    #                 'status': 'OK'
    #             }
    #     except Exception as ex:
    #         return {
    #             'status': repr(ex)
    #         }
    #
    # def read_db(self):
    #     """Выборка всех значений из базы данных
    #
    #     :return:
    #     """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT * FROM users")
    #         return result.fetchall()
    #
    # def user_exists(self, user_id):
    #     """Проверка существования пользователя
    #
    #     :param user_id: id пользователя
    #     :return:
    #     """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    #         return bool(result.fetchall())
    #
    # def set_username(self, user_id, username):
    #     """Отправка username-а пользователя
    #
    #     :param user_id: id пользователя
    #     :param username: username пользователя
    #     :return:
    #     """
    #     with self.connection:
    #         self.cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
    #         self.connection.commit()
    #         return True
    #
    # def get_signup(self, user_id):
    #     """Получение информации о том зарегистрирован ли пользователь
    #
    #     :param user_id: id пользователя
    #     :return:
    #     """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchall()
    #         return result[0][0]
    #
    # def delete_user(self, user_id):
    #     """Удаление пользователя
    #
    #     :param user_id: id пользователя
    #     :return:
    #     """
    #     with self.connection:
    #         self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    #         self.connection.commit()
    #         return True
    #
    # def set_signup(self, user_id, signup):
    #     """Подтверждение регистрации
    #
    #     :param user_id: id пользователя
    #     :param signup: done
    #     :return:
    #     """
    #     with self.connection:
    #         self.cursor.execute("UPDATE users SET signup = ? WHERE user_id = ?", (signup, user_id))
    #         self.connection.commit()
    #         return True
    #
    # def get_username(self, user_id):
    #     """Получение username-а пользователя
    #
    #     :param user_id: id пользователя
    #     :return:
    #     """
    #     with self.connection:
    #         result = self.cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,)).fetchall()
    #         return result[0][0]


if __name__ == '__main__':
    db = Database(fr'{BASE_DIR}/databases/bot.db', fr'{BASE_DIR}/databases/create_db.sql')

    for i in db.get_categories():
        print(i.name, i.codename)
