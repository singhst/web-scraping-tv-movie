import datetime
from mysql.connector import Error as mysqlError
import pandas as pd
from typing import List

from helperFunc import get_records_count

import logging

logger = logging.getLogger(__name__)


def insert_a_row(db_connection,
           table_name: str,
           rg_id: str,
           title: str,
           year: str, 
           rating: str,
           imdb_score: str, 
           reelgood_rating_score: str):

    print(f'> Inserting a record in `{db_connection.database}` database... ', end='')

    db_cursor = db_connection.cursor()

    sql_query = '''
        INSERT INTO ''' + table_name + ''' (
            rg_id,
            scraped_timestamp,
            title, 
            year, 
            rating, 
            imdb_score, 
            reelgood_rating_score
            ) 
        VALUES (%s, NOW(), %s, %s, %s, %s, %s);
    '''
    record = [(rg_id, title, year, rating, imdb_score, reelgood_rating_score)]

    try:
        old_row_count = get_records_count(db_cursor, table_name)
        # print('curr_row_count=', curr_row_count)

        db_cursor.executemany(sql_query, record)
        db_connection.commit()

        curr_row_count = get_records_count(db_cursor, table_name)

        print(f'==> Done!')
        print(f'> {db_cursor.rowcount} Record inserted successfully into Laptop table, {old_row_count}-row to {curr_row_count}-row')
        
        db_cursor.close()

    except(Exception, mysqlError) as error:
        print(f'\n\t==> Fail.')
        print(f'\t> Error = `{error}`')

    finally:
        if db_connection.is_connected():
            db_connection.close()
            print('> MySQL connection is closed')


def insert_n_rows(db_connection,
                  table_name: str,
                  df: pd.DataFrame
                  ):
    pass

def _add_panda_data_to_database(files: List[str], data_collector_func: callable, db_insert_func: callable, db_manager_func: callable):
    """
    Extract useful data from *.csv and add them to database

        Args:
            files (list): full paths
            data_collector_func (callable): function for collecting the data from files
            db_insert_func (callable): function for adding the data to database

        Returns:
            int: no. of rows added in all files
    """

    _total_added_rows = 0

    try:
        for _file in files:

            _start_time = datetime.datetime.now()
            _file_name = _get_filename_from_path(_file)
            logger.info('Start to process file ==> %s', _file_name)

            _df = data_collector_func(_file)

            _total_rows = len(_df.index)

            logger.info('Total rows=%s in %s', _total_rows, _file_name)

            _added_rows = 0
            _start_idx = 0

            if _total_rows == 0:
                # get the table name
                _rows, _table_name = db_insert_func([])
            else:
                while _start_idx < _total_rows:
                    _start_idx, _end_idx = _get_dataframe_slicing_end(
                        _total_rows, _start_idx, DB_BATCH_INSERT_SIZE)

                    _data = _df.loc[_start_idx:_end_idx, ]
                    _rows, _table_name = db_insert_func(
                        list(_df.loc[_start_idx:_end_idx, ].itertuples(index=False, name=None)))

                    _added_rows += _rows

                    _start_idx = _end_idx

            db_manager_func(_file_name, _table_name,
                            _total_rows, _added_rows, _start_time)

            logger.info('Total affected rows=%s in %s',
                        _added_rows, _file_name)
            _total_added_rows += _added_rows

    except Exception as e:
        logger.error("Unexpected error: %s", e)

    return _total_added_rows
