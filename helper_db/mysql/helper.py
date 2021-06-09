# database helper util

# get total number of records
def get_records_count(cursor):
    # execute the command
    cursor.execute('''SELECT * FROM employee;''')
    return len(cursor.fetchall())


# get by id
def get_by_id(cursor, eid):
    # sql query
    query = '''SELECT * FROM employee WHERE id = %s;'''
    # execute the command
    cursor.execute(query, [eid])
    return cursor.fetchone()
