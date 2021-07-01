from mysql.connector import Error as mysqlError
import math
import pandas as pd


def getRecordsCount(cursor, table_name: str):
    # execute the command
    cursor.execute(f'''SELECT * FROM {table_name};''')
    return len(cursor.fetchall())


# get by id
def get_by_id(cursor, 
              table_name: str, 
              eid: str):
    """Return the row by ID in database.
    """
    # sql query
    query = f'''SELECT * FROM {table_name} WHERE id = %s;'''
    # execute the command
    cursor.execute(query, [eid])
    return cursor.fetchone()


def updateColumnSize(db_connection, table_name: str, column_name: str, size: str) -> bool:
    print(f'mysql> Changing `{column_name}` column size in  `{table_name}` table in `{db_connection.database}` database... ', end='')
    
    x = math.ceil(math.log2(size))
    new_length = 2**x
    print(f'\n\t==> len({column_name})={size}, needs `varchar({new_length})`', end='')
    # creating a cursor to perform a sql operation
    db_cursor = db_connection.cursor()

    # sql query
    query = f'''ALTER TABLE {table_name} MODIFY {column_name} varchar({new_length});'''
    
    try:
        # execute the command
        db_cursor.execute(query)
        # commit the changes
        db_connection.commit()
        print('==> Done!')
    except(Exception, mysqlError) as error:
        print(f'\n\t==> Fail.')
        print(f'\t> Error = `{error}`')


# add 'id' column into df
def add_id_col_to_df(cursor, table_name: str, df: pd.DataFrame):
    """Add the `id` column into the df, the number of `id` is based on the existed rows in MySQL db.

    Arg
    ---
    `cursor`: MySQL cursor object

    `table_name`: `str`, the name of the table in database

    Return
    ---
    df inserted with `id` column.
    """

    start_id = getRecordsCount(cursor, table_name) + 1
    length = len(df)
    df.insert(0, 'id', [str(start_id+id) for id in range(length)])

    return df