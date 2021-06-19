from helper.translateToUrlPath import translateToUrlPath
from helper_db.databaseMysql.setupDatabase import setupDatabase
from helper_db.databaseMysql.createTable import createTable
from helper_db.databaseMysql.insert import insertARow, insertNRows, insertPandasDf


def getDataFromCsv():
    import pandas as pd
    df = pd.read_csv(
        '/Users/Sing/Documents/GitHub/web-scraping-tv-movie/reelgood-database/all-movies.csv')

    # last_col_index = len(df.columns) - 1
    df = df.iloc[:, 0:-1] #all rows, 
    df = df.head(12)
    df.insert(0, 'rg_id', 'x')
    df = df.applymap(str)  # change all columns dtype to string
    record = list(df.to_records(index=False))

    # print('df.dtypes =', df.dtypes)
    # print('record =', record)

    return df, record


if __name__ == '__main__':

    db_name = movies_or_tv = 'movies'  # 'tv' #
    db_table = 'movie'

    db = setupDatabase(db_name)
    db_connection = db.getConnection()

    createTable(db_connection, table_name=db_table)

    ####################################################################################

    print(f'\nbefore test_1(), db.isConnected() = {db.isConnected()}\n')

    def test_1():
        added_row_count = insertARow(db_connection,
                                     table_name=db_table,
                                     rg_id='4355a2e378-dfb0-4473-b105-7478bb1dcfc1',
                                     title='Se7en',
                                     year='1995',
                                     rating='18+',
                                     imdb_score='8.6/10',
                                     reelgood_rating_score='100/100',
                                     close_connection_afterward=False
                                     )
        print('> insertARow, added_row_count =', added_row_count)

    test_1()

    print(f'\nafter test_1(), db.isConnected() = {db.isConnected()}\n')

    ####################################################################################

    df, record = getDataFromCsv()

    def test_2():
        added_row_count = insertNRows(db_connection,
                                      table_name=db_table,
                                      record=record,
                                      close_connection_afterward=False
                                      )

        print('> insertNRows, added_row_count =', added_row_count)

    test_2()

    print(f'\nafter test_2(), db.isConnected() = {db.isConnected()}\n')

    ####################################################################################

    print('> df.head(10) =\n', df.head(10))

    def test_3():
        added_row_count = insertPandasDf(db_connection,
                                         table_name=db_table,
                                         df=df,
                                         close_connection_afterward=True
                                         )

        print('> insertPandasDf, added_row_count =', added_row_count)

    test_3()

    print(f'\nafter test_3(), db.isConnected() = {db.isConnected()}\n')
