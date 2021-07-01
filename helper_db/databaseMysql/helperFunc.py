# database helper util

# get total number of records
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