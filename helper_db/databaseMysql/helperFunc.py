# database helper util

# get total number of records
def getRecordsCount(cursor, table_name: str):
    # execute the command
    cursor.execute(f'''SELECT * FROM {table_name};''')
    return len(cursor.fetchall())