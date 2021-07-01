from typing import Iterable
from mysql.connector import Error as mysqlError


def checkCreateDataModel(db_connection) -> bool:
    """
    """
    print(f'mysql> Creating data model in `{db_connection.database}` database...')

    # Create `movie` table
    sql_query_movie_table, db_table_name = getMovieSqlQuery()
    checkCreateTable(db_connection, db_table_name=db_table_name, sql_query=sql_query_movie_table)
    
    # Create `availability` table
    sql_query_availability_table, db_table_name = getAvailabilitySqlQuery()
    checkCreateTable(db_connection, db_table_name=db_table_name, sql_query=sql_query_availability_table)


def getMovieSqlQuery() -> Iterable[str]:
    db_table_name = 'movie'
    query = f'''
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
            PRIMARY KEY(id)
        );
    '''
    return query, db_table_name


def getAvailabilitySqlQuery() -> Iterable[str]:
    db_table_name = 'availability'
    query = f'''
        CREATE TABLE IF NOT EXISTS {db_table_name} (
            link_id INT NOT NULL AUTO_INCREMENT,
            scraped_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rg_id VARCHAR(50) NOT NULL, 
            source_name VARCHAR(50) NOT NULL,
            source_movie_id VARCHAR(50),
            source_web_link VARCHAR(512),
            PRIMARY KEY(link_id)
        );
    '''
    return query, db_table_name


def checkCreateTable(db_connection,
                     db_table_name: str,
                     sql_query: str) -> bool:
    """
    """
    print(f'\t> Creating table `{db_table_name}` in `{db_connection.database}` database... ', end='')

    # creating database_cursor to perform SQL operation
    db_cursor = db_connection.cursor()

    try:
        db_cursor.execute(sql_query)
        print('==> Done!')

    except(Exception, mysqlError) as error:
        print(f'\n\t==> Fail.')
        print(f'\t> Error = `{error}`')

