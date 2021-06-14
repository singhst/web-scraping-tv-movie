# database helper util

# get total number of records
def get_records_count(cursor, table_name: str):
    # execute the command
    cursor.execute(f'''SELECT * FROM {table_name};''')
    return len(cursor.fetchall())