from Interfase.ISql import ISql
import pyodbc


class MsSql(ISql):

    def __init__(self, server, data_base, driver="ODBC Driver 13 for SQL Server"):
        self.__server = server
        self.__data_base = data_base
        self.__driver = driver
        self.__link = None
        self.__cursor = None

    @property
    def server(self):
        return self.__server

    @property
    def data_base(self):
        return self.__data_base

    @property
    def driver(self):
        return self.__driver

    @property
    def cursor(self):
        return self.__cursor

    @server.setter
    def server(self, val):
        self.__server = val

    @data_base.setter
    def data_base(self, val):
        self.__data_base = val

    @driver.setter
    def driver(self, val):
        self.__driver = val

    def create_link(self):
        self.__link = pyodbc.connect("DRIVER={" + self.__driver + "};"
                                     "Server=" + self.__server + ";"
                                     "Database=" + self.__data_base + ";"
                                     "Trusted_Connection=yes;")

        self.__cursor = self.__link.cursor()

    def destroy_link(self):
        self.__link.close()

    def commit_link(self):
        self.__link.commit()

    def name_column_table(self, name_table):
        self.__cursor.execute("EXEC sp_columns \"" + name_table + "\"")
        result = list(map(lambda x: x[3], self.__cursor.fetchall()))
        return result
