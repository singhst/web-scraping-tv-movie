import datetime
from re import T
from mysql.connector import Error as mysqlError
import pandas as pd
from typing import List

from helperFunc import getRecordsCount

import logging

logger = logging.getLogger(__name__)


def insertARow(db_connection,
                 table_name: str,
                 rg_id: str,
                 title: str,
                 year: str,
                 rating: str,
                 imdb_score: str,
                 reelgood_rating_score: str) -> int:

    """
    Public function. Add one record to MySQL database. 

        Args:
            db_connection:  `(class) MySQLConnection`, Connection to a MySQL Server
            table_name:     `str`, the table you want to insert data in
            ...... :        `str`, column titles in database

        Returns:
            int: no. of rows added to database
    """

    print(f'> Inserting a record in `{db_connection.database}` database... ', end='')

    record = [(rg_id, title, year, rating, imdb_score, reelgood_rating_score)]

    added_row_count = _tryAddRecordToDb(db_connection, table_name, record)

    return added_row_count


def insertNRows(db_connection,
                table_name: str,
                record: List[tuple]) -> int:
    """
    Public function. Add records to MySQL database. 

        Args:
            db_connection:  `(class) MySQLConnection`, Connection to a MySQL Server
            table_name:     `str`, the table you want to insert data in
            record:         `List[tuple]`, data to save into database
                            e.g. `[(data1, data2, ...), (...), ...]`

                            `pd.DataFrame().to_record()` converts df to List[turple]
        Returns:
            int: no. of rows added to database
    """
    print(f'> Inserting {len(record)} records in `{db_connection.database}` database... ', end='')

    added_row_count = _tryAddRecordToDb(db_connection, table_name, record)

    return added_row_count


def insertPandasDf(db_connection,
                table_name: str,
                df: pd.DataFrame) -> int:
    """
    Public function. Add records to MySQL database. 

        Args:
            db_connection:  `(class) MySQLConnection`, Connection to a MySQL Server
            table_name:     `str`, the table you want to insert data in
            record:         `List[tuple]`, data to save into database
                            e.g. `[(data1, data2, ...), (...), ...]`

                            `pd.DataFrame().to_records(index=False)` converts df to List[turple]
        Returns:
            int: no. of rows added to database
    """
    
    record = df.to_records(index=False)

    added_row_count = insertNRows(db_connection, table_name, record)

    return added_row_count


def _tryAddRecordToDb(db_connection,
                      table_name: str,
                      record: List[tuple]) -> int:
    """
    Private function. Add record(s) to MySQL database. 

        Args:
            db_connection:  `(class) MySQLConnection`, Connection to a MySQL Server
            table_name:     `str`, the table you want to insert data in
            record:         `List[tuple]`, data to save into database
                            e.g. `[(data1, data2, ...), (...), ...]`

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
            rating, 
            imdb_score, 
            reelgood_rating_score
            ) 
        VALUES''' + '(%s, NOW(), %s, %s, %s, %s, %s);'

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
    print(f'> {added_row_count} Record inserted successfully into `{table_name}` table, {old_row_count}th-row to {curr_row_count}th-row')

    db_cursor.close()

    # except(Exception, mysqlError) as error:
    #     print(f'\n\t==> Fail.')
    #     print(f'\t> Error = `{error}`')

    # finally:
    if db_connection.is_connected():
        db_connection.close()
        print('> MySQL connection is closed')

    return added_row_count