from connectMysql import database
  

def checkAndCreateDatabase(db_cursor, 
                           database_name: str) -> bool:
    """
    Return 
    ---
    `bool`

    `True`: Created the database in MySQL server

    `False`: Fail

    CREATE DATABASE IF NOT EXISTS DBName;

    """

    # executing cursor with execute method and pass SQL query
    db_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
    # get list of all databases
    db_cursor.execute("SHOW DATABASES")
    #print all databases
    for db in db_cursor:
        print(db)

if __name__ == "__main__":
    from connectMysql import database

    db = database()

    checkAndCreateDatabase()
