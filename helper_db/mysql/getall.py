# python mysql tutorial
# SQL SELECT - Get all records from the table

from connecttomysqldb import *
from helper import *


# get all records
def get_all(conn):
    # creating a cursor to perform a sql operation
    cursor = conn.cursor()

    # sql query
    query = '''SELECT * FROM employee;'''

    try:
        count = get_records_count(cursor)
        if count == 0:
            print('No data present in db')
        else:
            # execute the command
            cursor.execute(query)
            records = cursor.fetchall()

            print('EMPLOYEE INFORMATION')
            print('-------------------------------------')
            for record in records:
                full_name = record[1] + " " + record[2]
                print('Id = {}, Name = {}, Email = {}, Gender = {}, Phone = {}'.format(record[0], full_name,
                                                                                       record[3], record[4], record[5]))
    except(Exception, Error) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print('\nConnection closed')


# driver code
if __name__ == '__main__':
    # connect to database and get all data
    get_all(connect())
