# python mysql example
# SQL operation - Delete all records from the table

from connecttomysqldb import *
from helper import *


# delete all record
def delete_all(conn):
    # creating a cursor to perform a sql operation
    cursor = conn.cursor()

    # sql query
    query = '''DELETE FROM employee;'''

    try:
        count = get_records_count(cursor)
        if count == 0:
            print('No data present in db. Skipping delete all')
        else:
            # execute the command
            cursor.execute(query)
            # commit the changes
            conn.commit()

            print('All data deleted successfully')
    except(Exception, Error) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print('\nConnection closed')


# driver code
if __name__ == '__main__':
    # connect to database and delete all records
    delete_all(connect())
