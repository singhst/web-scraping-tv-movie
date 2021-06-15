from mysql.connector import Error as mysqlError


def createTable(db_connection, table_name: str):
    """
    """
    print(f'> Creating table `{table_name}` in `{db_connection.database}` database... ')

    # creating database_cursor to perform SQL operation
    db_cursor = db_connection.cursor()
    
    # sql query
    #"rg_id": "55a2e378-dfb0-4473-b105-7478bb1dcfc1",
    sql_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            rg_id VARCHAR(50) NOT NULL, 
            scraped_date Date NOT NULL DEFAULT now(),
            scraped_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title VARCHAR(255), 
            description VARCHAR(512),
            year INT, 
            rating VARCHAR(10), 
            imdb_score VARCHAR(10),     
            reelgood_rating_score VARCHAR(10),
            PRIMARY KEY(rg_id)
        );
    '''

    try:
        db_cursor.execute(sql_query)
        print('\t==> Done!')

    except(Exception, mysqlError) as error:
        print(f'\t==> Fail.')
        print(f'\t> Error = `{error}`')
