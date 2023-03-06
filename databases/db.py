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
