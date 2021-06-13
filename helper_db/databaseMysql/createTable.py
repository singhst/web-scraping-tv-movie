
def createTable(db_connection):
    """
    """

    # creating database_cursor to perform SQL operation
    db_cursor = db_connection.cursor()
    db_connection

    sql_query = '''
        CREATE TABLE IF NOT EXIST 
    '''