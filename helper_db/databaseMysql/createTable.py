from mysql.connector import Error as mysqlError


def createTable(db_connection, table_name: str):
    """
    """
    print(f'> Creating table `{table_name}` in `{db_connection.database}` database... ', end='')

    # creating database_cursor to perform SQL operation
    db_cursor = db_connection.cursor()
    
    # sql query
    sql_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT NOT NULL, 
            Title VARCHAR(255), 
            Year INT, 
            Rating INT, 
            IMDBScore INT, 
            ReelgoodRatingScore INT
        );
    '''

    try:
        db_cursor.execute(sql_query)
        print('==> Done!')

    except(Exception, mysqlError) as error:
        print(f'> Error = `{error}`')