"""
Insert data into the table
"""

import datetime
from re import T
from mysql.connector import Error as mysqlError
import pandas as pd
from typing import List

from helperFunc import getRecordsCount

import logging

logger = logging.getLogger(__name__)


def insertARowToDb(db_connection,
               table_name: str,
               rg_id: str,
               title: str,
               year: str,
               overview: str,
               rating: str,
               imdb_score: str,
               reelgood_rating_score: str,
               close_connection_afterward: bool = True) -> int:
    """
    Public function. Add one record to MySQL database. 

        Args:
            db_connection:  `(class) MySQLConnection`, Connection to a MySQL Server
            table_name:     `str`, the table you want to insert data in
            ...... :        `str`, column titles in database
            close_connection_afterward:     `bool`, default `True`. Choose to close `cursor` and `mysql connection` after operation.

        Returns:
            `int`: no. of rows added to database
    """

    print(f'mysql> Inserting a record into `{table_name}` table in `{db_connection.database}` database... ', end='')

    record = [(rg_id, title, year, overview, rating, imdb_score, reelgood_rating_score)]

    added_row_count = _tryAddRecordToDb(db_connection, table_name, record, close_connection_afterward)

    return added_row_count


def insertNRowsToDb(db_connection,
                    table_name: str,
                    record: List[tuple],
                    close_connection_afterward: bool = True) -> int:
    """
    Public function. Add records to MySQL database. 

        Args:
            db_connection:  `(class) MySQLConnection`, Connection to a MySQL Server
            table_name:     `str`, the table you want to insert data in
            record:         `List[tuple]`, data to save into database
                            e.g. `[(data1, data2, ...), (...), ...]`
                            
                            `record = [(rg_id, title, year, overview, rating, imdb_score, reelgood_rating_score)]`

                            `pd.DataFrame().to_record()` converts df to List[turple]

            close_connection_afterward:     `bool`, default `True`. Choose to close `cursor` and `mysql connection` after operation.

        Returns:
            `int`: no. of rows added to database
    """
    print(f'mysql> Inserting {len(record)} record into `{table_name}` table in `{db_connection.database}` database... ', end='')


    added_row_count = _tryAddRecordToDb(db_connection, table_name, record, close_connection_afterward)

    return added_row_count


def insertPandasDfToDb(db_connection,
                       table_name: str,
                       df: pd.DataFrame,
                       close_connection_afterward: bool = True) -> int:
    """
    Public function. Add records to MySQL database. 

        Args:
            db_connection:  `(class) MySQLConnection`, Connection to a MySQL Server
            table_name:     `str`, the table you want to insert data in
            record:         `List[tuple]`, data to save into database
                            e.g. `[(data1, data2, ...), (...), ...]`

                            `record = [(rg_id, title, year, overview, rating, imdb_score, reelgood_rating_score)]`

                            `pd.DataFrame().to_records(index=False)` converts df to List[turple]

            close_connection_afterward:     `bool`, default `True`. Choose to close `cursor` and `mysql connection` after operation.

        Returns:
            `int`: no. of rows added to database
    """

    record = list(df.to_records(index=False))

    added_row_count = insertNRowsToDb(db_connection, table_name, record, close_connection_afterward)

    return added_row_count


def _tryAddRecordToDb(db_connection,
                      table_name: str,
                      record: List[tuple],
                      close_connection_afterward: bool) -> int:
    """
    Private function. Add record(s) to MySQL database. 

        Args:
            db_connection:  `(class) MySQLConnection`, Connection to a MySQL Server
            table_name:     `str`, the table you want to insert data in
            record:         `List[tuple]`, data to save into database
                            e.g. `[(data1, data2, ...), (...), ...]`
            close_connection_afterward:     `bool`, default `True`. Choose to close `cursor` and `mysql connection` after operation.

        Returns:
            int: no. of rows added to database
    """

    db_cursor = db_connection.cursor()

    sql_query = f'''
        INSERT INTO {table_name} (
            rg_id,
            scraped_timestamp,
            title, 
            year, 
            overview,
            rating, 
            imdb_score, 
            reelgood_rating_score,
            url_offset_value
            ) 
        VALUES''' + '(%s, NOW(), %s, %s, %s, %s, %s, %s, %s);'

    added_row_count = 0

    # try:
    old_row_count = getRecordsCount(db_cursor, table_name)
    # db_cursor.rowcount
    # print('curr_row_count=', curr_row_count)

    db_cursor.executemany(sql_query, record)
    db_connection.commit()

    curr_row_count = getRecordsCount(db_cursor, table_name)

    added_row_count = curr_row_count - old_row_count

    print(f'==> Done!')
    print(f'mysql> {added_row_count} Record inserted successfully into `{table_name}` table, {old_row_count}th-row to {curr_row_count}th-row')

    # db_cursor.close()

    # except(Exception, mysqlError) as error:
    #     print(f'\n\t==> Fail.')
    #     print(f'\t> Error = `{error}`')

    # finally:
    if close_connection_afterward:
        db_cursor.close()
        if db_connection.is_connected():
            db_connection.close()
            print('mysql>>> MySQL connection is closed\n')

    return added_row_count
