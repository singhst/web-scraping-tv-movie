# python mysql example
# SQL operation - Delete a record from the table

from connecttomysqldb import *
from helper import *


# delete a record
def delete(conn, eid):
    # creating a cursor to perform a sql operation
    cursor = conn.cursor()

    # sql query
    query = '''DELETE FROM employee WHERE id = %s;'''

    try:
        record = get_by_id(cursor, eid)
        if record is None:
            print('Employee id = {} not found'.format(eid))
        else:
            # execute the command
            cursor.execute(query, [eid])
            # commit the changes
            conn.commit()

            print('Employee id = {} deleted successfully'.format(eid))
    except(Exception, Error) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print('\nConnection closed')


# driver code
if __name__ == '__main__':
    # connect to database and delete a record
    delete(connect(), 5)
