from Interfase.ISql import ISql
import sqlite3 as sq
from os.path import join, dirname, abspath
from os import getcwd


class SqlLite(ISql):

    def __init__(self, name_db, path=None):
        self.__name_db = name_db
        self.__path = path
        self.__link = None
        self.__cursor = None

    @property
    def name_db(self):
        return self.__name_db

    @property
    def cursor(self):
        return self.__cursor

    @name_db.setter
    def name_db(self, val):
        self.__name_db = val

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, val):
        self.__path = val

    def create_link(self):
        name = self.__name_db
        if self.__path is not None:
            name = join(self.__path, self.__name_db)
        else:
            base_dir = dirname(abspath(getcwd()))
            name = join(base_dir, name)
        self.__link = sq.connect(name)
        self.__cursor = self.__link.cursor()

    def destroy_link(self):
        self.__link.close()

    def commit_link(self):
        self.__link.commit()

    def name_column_table(self, name_table):
        self.__cursor.execute("PRAGMA table_info(" + name_table + ")")
        result = list(map(lambda x: x[1], self.__cursor.fetchall()))
        return result
