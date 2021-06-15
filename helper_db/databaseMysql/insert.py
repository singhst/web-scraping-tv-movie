from mysql.connector import Error as mysqlError

from helperFunc import get_records_count


def insert_a_row(db_connection,
           table_name: str,
           rg_id: str,
           title: str,
           year: str, 
           rating: str,
           imdb_score: str, 
           reelgood_rating_score: str):

    print(f'> Inserting a record in `{db_connection.database}` database... ')

    db_cursor = db_connection.cursor()

    sql_query = '''
        INSERT INTO ''' + table_name + ''' (rg_id, title, year, rating, imdb_score, reelgood_rating_score) VALUES (%s, %s, %s, %s, %s, %s);
    '''
    record = (rg_id, title, year, rating, imdb_score, reelgood_rating_score)

    try:
        curr_row_count = get_records_count(db_cursor, table_name)
        print('curr_row_count=', curr_row_count)

        db_cursor.execute(sql_query, record)
        db_connection.commit()
        print(">", db_cursor.rowcount, "Record inserted successfully into Laptop table")
        db_cursor.close()

        print(f'\t==> Done!')

    except(Exception, mysqlError) as error:
        print(f'\t==> Fail.')
        print(f'\t> Error = `{error}`')

    finally:
        if db_connection.is_connected():
            db_connection.close()
            print('> MySQL connection is closed')


def insert_n_rows(db_connection,
                  table_name: str,
                  ):
    pass