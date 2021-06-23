"""
Get records from the table

returns dict if `dictionary is True` 
==> https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-cursor.html

"""


import json
from mysql.connector import Error as mysqlError
from typing import List

from helperFunc import getRecordsCount


# get all records
def readTableAll(db_connection,
                 table_name: str,
                 close_connection_afterward: bool = True) -> List[tuple]:
    """
    Public function. Query full table data. 

        Args
        ---
            db_connection:  `(class) MySQLConnection`, Connection to a MySQL Server
            table_name:     `str`, the table you want to insert data in
            close_connection_afterward:     `bool`, default `True`. Choose to close `db_cursor` and `mysql connection` after operation.

        Queried result from MySQL
        ---
            `List[tuple]`:  e.g. `[(id, column1, column2, ...), (...), ...]`

        Return
        ---
            
            `Iterable[dict]`, a `list of dict` in json format.

            e.g.

            [
                {'Title': 'Breaking Bad', 'Year': 2008},

                {'Title': 'Game of Thrones', 'Year': 2011},
                
                ...
            ]

        Remark
        ------
            
            `json.dumps(the_return_dict_list)` make return dict become JSON string.
    """

    print(f'mysql> Reading records from `{table_name}` table in `{db_connection.database}` database... ', end='')

    # creating a db_cursor to perform a sql operation
    # returns dict list if `dictionary is True` ==> https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-cursor.html
    db_cursor = db_connection.cursor(dictionary=True)

    # sql query
    query = f'''SELECT * FROM {table_name};'''

    record = None

    try:
        count = getRecordsCount(cursor=db_cursor, table_name=table_name)
        if count == 0:
            print(f'\n\t==> Fail.')
            print(f'\tmysql> No data present in `{table_name}` table in `{db_connection.database}` database.')
        else:
            # execute the command
            db_cursor.execute(query)
            db_cursor
            record = db_cursor.fetchall()
            print(f'==> Done!')
            
    except(Exception, mysqlError) as error:
        print(f'\n\t==> Fail.')
        print(f'\t> Error = `{error}`')
    

    if close_connection_afterward:
        if db_connection.is_connected():
            db_cursor.close()
            db_connection.close()
            print('mysql>>> MySQL connection is closed\n')

    return record #json.dumps(record, indent=4, sort_keys=True, default=str)


# driver code
# if __name__ == '__main__':
#     # connect to database and get all data
#     readTableAll(connect())
