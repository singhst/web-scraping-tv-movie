# python mysql

import mysql.connector
from mysql.connector import Error

from readdbconfig import *


def connect():
    try:
        # method will read the env file and return the config object
        params = read_db_params()

        # connect to database
        # reading the database parameters from the config object
        conn = mysql.connector.connect(
            host=params.get('DB', 'host'),
            database=params.get('DB', 'database'),
            user=params.get('DB', 'username'),
            password=params.get('DB', 'password'),
            port=params.get('DB', 'port')
        )

        return conn
    except(Exception, Error) as error:
        print(error)
