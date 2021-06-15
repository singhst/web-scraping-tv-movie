"""
Make connection to MySQL server and gets all config parameters. 


Error code handling example,
=> https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-error.html

MySQL error code,
=> https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html
"""


import mysql.connector
from mysql.connector import Error as mysqlError
from mysql.connector import errorcode, errors

from configparser import Error as configError

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
sys.path.append(currentdir)
from readConfig import readConfig


class setupDatabase():
    """
    
    ---

    `(class) MySQLConnection`, Connection to a MySQL Server
    
    `(class) CMySQLCursor`, Cursor to perform SQL operation

    `(str) Database name`

    """

    def __init__(self, 
                 db_name: str) -> None:

        self.db_config = ''

        self.host = ''
        self.database = db_name
        self.user = ''
        self.password = ''
        self.port = ''

        self.db_connection = ''
        self.db_cursor = ''

        self.importDbConfig()
        self.connectServer()
        self.checkCreateDatabase()
        self.usingDb()


    def importDbConfig(self):

        print(f'> Reading MySQL .env config file... ', end='')

        try:
            self.db_config = readConfig()

            self.host = self.db_config.get('DB', 'host')
            # self.database = self.db_config.get('DB', 'database')
            self.user = self.db_config.get('DB', 'username')
            self.password = self.db_config.get('DB', 'password')
            self.port = self.db_config.get('DB', 'port')

            print('==> Done!')

        except(Exception, configError) as error:
            print(f'\t> Error. Error code = `{error}`')


    def connectServer(self) -> None:
        """
        Return
        ------
        `(class) MySQLConnection`

        Connection to a MySQL Server
        """
        print(f'> Connecting to MySQL server... ', end='')
        try:
            self.db_connection = mysql.connector.connect(
                host = self.host,
                # database = self.database,
                user = self.user,
                password = self.password,
                port = self.port
            )
            print('==> Done!')

            # creating database_cursor to perform SQL operation
            self.db_cursor = self.db_connection.cursor()

            return None
            
        except(Exception, mysqlError) as error:
            print(f'\n\t==> Fail.')
            print(f'\t> Error = `{error}`')


    def checkCreateDatabase(self) -> bool:
        """

        CREATE DATABASE IF NOT EXISTS DBName;

        """
        print(f'> Created database `{self.database}`... ', end='')

        # executing cursor with execute method and pass SQL query
        sql_query = f"CREATE DATABASE IF NOT EXISTS {self.database};"
        self.db_cursor.execute(sql_query)

        print(f'==> Done!')


    def usingDb(self):
        print(f'> Using database `{self.database}`... ', end='')
        try:
            self.db_connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password,
                port = self.port
            )
            print('==> Done!')

            # creating database_cursor to perform SQL operation
            self.db_cursor = self.db_connection.cursor()

            return None
            
        except(Exception, mysqlError) as error:
            print(f'\n\t==> Fail.')
            print(f'\t> Error = `{error}`')


    def getDbList(self):
        # get list of all databases
        self.db_cursor.execute("SHOW DATABASES")
        #print all databases
        for db in self.db_cursor:
            print(db)


    def getConnection(self):
        """
        Return 
        ---

        `(class) MySQLConnection`, Connection to a MySQL Server
        """
        
        return self.db_connection


    def getDbName(self):
        """
        Return 
        ---

        `(str) Database name`
        """
    
        return self.database


if __name__ == "__main__":
    
    db_name = 'movies'

    db = setupDatabase(db_name)
    db_connection = db.getConnection()
