# python mysql
# SQL operation - Update record in table

from mysql.connector import Error as mysqlError
from typing import List

from helperFunc import get_by_id


# update a record
def updateRowById(db_connection,
                  table_name: str,
                  eid: str,
                  title: str,
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
    # creating a cursor to perform a sql operation
    db_cursor = db_connection.cursor()

    # sql query
    query = f'''UPDATE {table_name} SET rg_id = %s, overview = %s WHERE id = %s AND title = %s;'''

    try:
        record = get_by_id(cursor=db_cursor, table_name=table_name, eid=eid)
        if record is None:
            print(f'mysql> Movie id = `{eid}`, title = `{title}` not found')
        else:
            # execute the command
            db_cursor.execute(query, [rg_id, overview, eid, title])
            # commit the changes
            db_connection.commit()

            print(f'mysql> {table_name} id = `{eid}`, title = `{title}` updated successfully')
    except(Exception, mysqlError) as error:
        print(f'\n\t==> Fail.')
        print(f'\t> Error = `{error}`')
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
