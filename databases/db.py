import logging
import sqlite3 as sq
from sqlite3 import OperationalError, IntegrityError
from typing import NamedTuple

from config.bot_config import BASE_DIR, LOGGER

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
        self.connection.execute("PRAGMA foreign_keys = ON")
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
                result = self.cursor.execute("SELECT name, codename "
                                             "FROM categories")
                for category in result:
                    result = Category(name=category[0].title(), codename=category[1])
                    yield result
        except Exception as ex:
            logging.error(repr(ex))

    def add_expense(self, user_id: int, amount: float, category_codename: str) -> None:
        """Adding an expense

        :param user_id: user id
        :param amount: expense amount
        :param category_codename: expense category code
        :return: None
        """
        try:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO expense (id, amount, created, category_codename)"
                    "VALUES (?, ?, datetime('now', 'localtime'), ?)",
                    (user_id, amount, category_codename))
        except IntegrityError as ex:
            logging.error(repr(ex))

        except Exception as ex:
            logging.error(repr(ex))

    def _check_user(self, user_id: int) -> bool or None:
        """Checking if a user exists

        :param user_id: user_id
        :return: True/None
        """
        with self.connection:
            users = self.cursor.execute('SELECT id '
                                        'FROM users '
                                        'WHERE id = ?', (user_id,)).fetchall()
            if not users:
                return True
            else:
                return

    def add_user(self, user_id: int, is_admin: bool) -> None:
        """Adding a user to the database

        :param is_admin: bool
        :param user_id: user id
        :return: None
        """
        try:
            with self.connection:
                if self._check_user(user_id=user_id):
                    self.cursor.execute(
                        "INSERT INTO users (id, is_admin, is_active, last_active)"
                        "VALUES (?, ?, ?, datetime('now', 'localtime'))",
                        (user_id, True, is_admin))
                    logging.info(f'Add new user {user_id}')
        except IntegrityError:
            logging.info(f'Data not saved, such user [{user_id}] already exists')

    def update_last_active(self, user_id: int) -> None:
        """Update last user activity

        :param user_id: user id
        :return: None
        """
        try:
            with self.connection:
                if not self._check_user(user_id=user_id):
                    self.cursor.execute("UPDATE users "
                                        "SET last_active = datetime('now', 'localtime')"
                                        "WHERE id = ?",
                                        (user_id,))
        except Exception as ex:
            logging.error(repr(ex))
