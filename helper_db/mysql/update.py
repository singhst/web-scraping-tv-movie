# python mysql
# SQL operation - Update record in table

from connecttomysqldb import *
from helper import *


# update a record
def update(conn, eid):
    # creating a cursor to perform a sql operation
    cursor = conn.cursor()

    # sql query
    query = '''UPDATE employee SET gender = %s WHERE id = %s;'''

    try:
        record = get_by_id(cursor, eid)
        if record is None:
            print('Employee id = {} not found'.format(eid))
        else:
            # execute the command
            cursor.execute(query, ['F', eid])
            # commit the changes
            conn.commit()

            print('Employee id = {} updated successfully'.format(eid))
    except(Exception, Error) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print('\nConnection closed')


# driver code
if __name__ == '__main__':
    # connect to database and update a record
    update(connect(), 5)
