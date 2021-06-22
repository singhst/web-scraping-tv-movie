# database helper util

# get total number of records
def getRecordsCount(cursor, table_name: str):
    # execute the command
    cursor.execute(f'''SELECT * FROM {table_name};''')
    return len(cursor.fetchall())

# get by id
def get_by_id(cursor, 
              table_name: str, 
              eid: str):
    """Return the row by ID in database.
    """
    # sql query
    query = f'''SELECT * FROM {table_name} WHERE id = %s;'''
    # execute the command
    cursor.execute(query, [eid])
    return cursor.fetchone()