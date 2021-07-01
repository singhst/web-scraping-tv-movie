# python mysql
# SQL operation - Update record in table

from mysql.connector import Error as mysqlError
from mysql.connector import errorcode
from typing import List

from helperFunc import get_by_id, updateColumnSize


# update a record
def updateRowById(db_connection,
                  table_name: str,
                  eid: str,
                  title: str,
                  year: str,
                  rg_id: str,
                  overview: str,
                  close_connection_afterward: bool = True) -> List[tuple]:
    """
    Public function. Query full table data. 

        Args:
            db_connection:  `(class) MySQLConnection`, Connection to a MySQL Server
            table_name:     `str`, the database table you want to insert data to 
            title:          `str`, 
            rg_id:          `str`, ID used by Reelgoog
            overview:       `str`, description of the movie/TV show
            close_connection_afterward:     `bool`, default `True`. Choose to close `cursor` and `mysql connection` after operation.

        Returns:
            `List[tuple]`:  Data queried from database.
                            e.g. `[(id, column1, column2, ...), (...), ...]`
    """
    print(f'mysql> Updating id = `{eid}`, title = `{title}` in  `{table_name}` table in `{db_connection.database}` database... ', end='')
    
    # creating a cursor to perform a sql operation
    db_cursor = db_connection.cursor()

    # sql query
    query = f'''UPDATE {table_name} SET rg_id = %s, overview = %s WHERE title = %s AND year = %s;'''

    try:
        record = get_by_id(cursor=db_cursor, table_name=table_name, eid=eid)
        if record is None:
            print(f'\n\t==> Fail.')
            print(f'\t> Movie id = `{eid}`, title = `{title}`, year = `{year}` not found')
        else:
            # execute the command
            db_cursor.execute(query, [rg_id, overview, title, year])
            # commit the changes
            db_connection.commit()

            print('==> Done!')
    except(Exception, mysqlError) as error:
        print(f'\n\t==> Fail.')
        print(f'\t> Error = `{error}`')

        # if scraped string in `overview` column is too long, increase its Column Size.
        if error.errno == errorcode.ER_DATA_TOO_LONG:
            start_index = error.msg.find('column \'') + len('column \'')
            end_index = error.msg.find('\' at')
            column_name = error.msg[start_index:end_index]
            print(f'\t> column_name = error.msg[start_index:end_index] = `{column_name}`.')
            updateColumnSize(db_connection=db_connection, table_name=table_name, column_name=column_name, size=len(overview))
            #recursion, try update the row again
            updateRowById(db_connection=db_connection,
                          table_name=table_name,
                          eid=eid,
                          title=title,
                          year=year,
                          rg_id=rg_id,
                          overview=overview,
                          close_connection_afterward=False)
    finally:
        if close_connection_afterward:
            if db_connection is not None:
                db_cursor.close()
                db_connection.close()
                print('mysql>>> MySQL connection is closed\n')


# driver code
if __name__ == '__main__':
    # connect to database and update a record
    # update(connect(), 5)
    pass
