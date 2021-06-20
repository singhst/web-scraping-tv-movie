from helper.translateToUrlPath import translateToUrlPath
from helper_db.databaseMysql.setupDatabase import setupDatabase
from helper_db.databaseMysql.insert import insertARowToDb, insertNRowsToDb, insertPandasDfToDb
from helper_db.databaseMysql.readTable import readTableAll


def getDataFromCsv():
    import pandas as pd
    df = pd.read_csv(
        '/Users/Sing/Documents/GitHub/web-scraping-tv-movie/reelgood-database/all-movies.csv')

    # last_col_index = len(df.columns) - 1
    df = df.iloc[:, 0:-1] #remove last column 'Available On'; get all rows, 1st col to (last - 1) col
    df = df.head(12)
    df.insert(0, 'rg_id', '')
    df.insert(3, 'overview', '')
    df = df.applymap(str)  # change all columns dtype to string
    record = list(df.to_records(index=False))

    # print('df.dtypes =', df.dtypes)
    # print('record =', record)

    return df, record


def test_setupdatabase_and_insert():

    db_name = movies_or_tv = 'test_movies'  # 'tv' #
    db_table = 'test_movie'

    db = setupDatabase(db_name, db_table)
    db_connection = db.getConnection()

    # checkCreateTable(db_connection, table_name=db_table)

    ################################################################################################

    print(f'\nbefore test_1(), db.isConnected() = {db.isConnected()}\n')

    def test_1():
        added_row_count = insertARowToDb(db_connection,
                                     table_name=db_table,
                                     rg_id='4355a2e378-dfb0-4473-b105-7478bb1dcfc1',
                                     title='Se7en',
                                     year='1995',
                                     overview='',
                                     rating='18+',
                                     imdb_score='8.6/10',
                                     reelgood_rating_score='100/100',
                                     close_connection_afterward=False
                                     )
        print('> insertARowToDb, added_row_count =', added_row_count)

    test_1()

    print(f'\nafter test_1(), db.isConnected() = {db.isConnected()}\n')

    ################################################################################################

    df, record = getDataFromCsv()

    def test_2():
        added_row_count = insertNRowsToDb(db_connection,
                                      table_name=db_table,
                                      record=record,
                                      close_connection_afterward=False
                                      )

        print('> insertNRowsToDb, added_row_count =', added_row_count)

    test_2()

    print(f'\nafter test_2(), db.isConnected() = {db.isConnected()}\n')

    ################################################################################################

    print('> df.head(10) =\n', df.head(10))

    def test_3():
        added_row_count = insertPandasDfToDb(db_connection,
                                         table_name=db_table,
                                         df=df,
                                         close_connection_afterward=True
                                         )

        print('> insertPandasDfToDb, added_row_count =', added_row_count)

    test_3()

    print(f'\nafter test_3(), db.isConnected() = {db.isConnected()}\n')


if __name__ == '__main__':

    test_setupdatabase_and_insert()
