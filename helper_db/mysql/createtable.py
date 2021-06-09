# python mysql example
# SQL operation - Create a table

from connecttomysqldb import *


# create table method
def create_table(conn):
    # creating a cursor to perform a sql operation
    cursor = conn.cursor()

    # sql query
    query = '''
    CREATE TABLE employee (id INT NOT NULL, first_name VARCHAR(255), 
    last_name VARCHAR(100), email VARCHAR(150), 
    gender VARCHAR(50), phone VARCHAR(100), 
    PRIMARY KEY (id));
    '''

    try:
        # execute the command
        cursor.execute(query)
        # commit the changes
        conn.commit()

        print('Table created successfully')
    except(Exception, Error) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print('\nConnection closed')


# driver code
if __name__ == '__main__':
    # connect to database and create table
    create_table(connect())
