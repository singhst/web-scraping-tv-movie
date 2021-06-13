"""

Error code handling example,
=> https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-error.html

MySQL error code,
=> https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html
"""


import mysql.connector
from mysql.connector import Error as mysqlError
from mysql.connector import errorcode, errors

from configparser import Error as configError

from readConfig import readConfig
import createDatabase


class database():

    def __init__(self) -> None:

        self.db_config = ''

        self.host = ''
        self.database = ''
        self.user = ''
        self.password = ''
        self.port = ''

        self.db_connection = ''
        self.db_cursor = ''

        self.importDbConfig()


    def importDbConfig(self):

        print(f'> Reading MySQL .env config file... ', end='')

        try:
            self.db_config = readConfig()

            self.host = self.db_config.get('DB', 'host')
            self.database = self.db_config.get('DB', 'database')
            self.user = self.db_config.get('DB', 'username')
            self.password = self.db_config.get('DB', 'password')
            self.port = self.db_config.get('DB', 'port')

            print('==> Done!')

        except(Exception, configError) as error:
            print(f'> Error. Error code = `{error}`')
            pass
        

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
            print(f'==> Connection fail. Error = `{error}`')
            return None


def connectMysql():
    """
    Return 
    ---
    (MySQLConnection, CMySQLCursor)

    `(class) MySQLConnection`, Connection to a MySQL Server

    `(class) CMySQLCursor`, Cursor to perform SQL operation
    """

    db = database()
    db.connectServer()

    database_name = db.database
    database_cursor = db.db_cursor

    if createDatabase.checkAndCreateDatabase(database_cursor, database_name):
        print(f'> Create database `{database_name}`.')
    
    return db.db_connection


if __name__ == "__main__":
    connectMysql()
