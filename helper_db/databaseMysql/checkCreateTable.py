from mysql.connector import Error as mysqlError


def checkCreateTable(db_connection,
                     db_table_name: str) -> bool:
    """
    """
    print(f'mysql> Creating table `{db_table_name}` in `{db_connection.database}` database... ', end='')

    # creating database_cursor to perform SQL operation
    db_cursor = db_connection.cursor()
    
    # sql query
    #"rg_id": "55a2e378-dfb0-4473-b105-7478bb1dcfc1",
    sql_query = f'''
        CREATE TABLE IF NOT EXISTS {db_table_name} (
            id INT NOT NULL AUTO_INCREMENT,
            scraped_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rg_id VARCHAR(50) NOT NULL, 
            title VARCHAR(255), 
            year INT, 
            overview VARCHAR(512),
            rating VARCHAR(10), 
            imdb_score VARCHAR(10),     
            reelgood_rating_score VARCHAR(10),
            url_offset_value INT,
            PRIMARY KEY(id, rg_id)
        );
    '''

    try:
        db_cursor.execute(sql_query)
        print('==> Done!')

    except(Exception, mysqlError) as error:
        print(f'\n\t==> Fail.')
        print(f'\t> Error = `{error}`')
