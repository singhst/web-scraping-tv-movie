from helper.translateToUrlPath import translateToUrlPath
from helper_db.databaseMysql.setupDatabase import setupDatabase
from helper_db.databaseMysql.createTable import createTable
from helper_db.databaseMysql.insert import insertARow, insertNRows


def test_1():
    # 55a2e378-dfb0-4473-b105-7478bb1dcfc1
    # Se7en,
    # 1995,
    # 18+,
    # 8.6/10,
    # 100/100,
    # + Rent or Buy
    added_row_count = insertARow(db_connection, 
                table_name=db_table, 
                rg_id= '4355a2e378-dfb0-4473-b105-7478bb1dcfc1',
                title='Se7en', 
                year='1995', 
                rating='18+',
                imdb_score='8.6/10',
                reelgood_rating_score='100/100')

    print('> insertARow, added_row_count =', added_row_count)


def test_2():

    import pandas as pd
    df = pd.read_csv('/Users/Sing/Documents/GitHub/web-scraping-tv-movie/reelgood-database/all-movies.csv')

    last_col_index = len(df.columns) - 1
    df = df.iloc[:, 0:-1]
    df = df.head(12)
    df.insert(0, 'rg_id', '')
    df = df.applymap(str)
    record = list(df.to_records(index=False))

    print('df.dtypes =', df.dtypes)
    print('record =', record)

    added_row_count = insertNRows(db_connection,
                table_name = db_table, 
                record = record
                )

    print('> insertARow, added_row_count =', added_row_count)


if __name__ == '__main__':

    db_name = movies_or_tv = 'movies' # 'tv' #
    db_table = 'movie'

    db = setupDatabase(db_name)
    db_connection = db.getConnection()

    createTable(db_connection, table_name=db_table)

    test_1()

    db = setupDatabase(db_name)
    db_connection = db.getConnection()

    test_2()