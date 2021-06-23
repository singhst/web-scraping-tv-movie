from helper.translateToUrlPath import translateToUrlPath
from helper_db.databaseMysql.setupDatabase import setupDatabase
from helper_db.databaseMysql.insert import insertARowToDb, insertNRowsToDb, insertPandasDfToDb
from helper_db.databaseMysql.readTable import readTableAll
from helper_db.databaseMysql.update import updateRowById


def getDataFromCsv():
    import pandas as pd
    df = pd.read_csv(
        '/Users/Sing/Documents/GitHub/web-scraping-tv-movie/reelgood-database/all-movies.csv')

    # last_col_index = len(df.columns) - 1
    # remove last column 'Available On'; get all rows, 1st col to (last - 1) col
    df = df.iloc[:, 0:-1]
    df = df.head(12)
    df.insert(0, 'rg_id', 'n/a')
    df.insert(3, 'overview', 'n/a')
    df = df.loc[:, df.columns != 'available on']    #remove last column 'Available On'
    df = df.applymap(str)  # change all columns dtype to string
    url_offset_value = -123
    df['url_offset_value'] = str(url_offset_value)

    record = list(df.to_records(index=False))

    print('> list(df.columns) =\n', list(df.columns))
    print('> df.head(2) =\n', df.head(2))
    print('> len(record[0]) =', len(record[0]))

    return df, record


def test_setupdatabase_and_insert():

    db_name = movies_or_tv = 'test_movies'  # 'tv' #
    db_table = 'test_movie'

    db = setupDatabase(db_name, db_table)
    db_connection = db.getConnection()

    # checkCreateTable(db_connection, table_name=db_table)

    ################################################################################################
    print('\n### test_1() #############################################################################################')

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
                                         url_offset_value = '-1',
                                         close_connection_afterward=False
                                         )
        print('> insertARowToDb, added_row_count =', added_row_count)

    test_1()

    print(f'\nafter test_1(), db.isConnected() = {db.isConnected()}\n')

    ################################################################################################
    print('\n### test_2() #############################################################################################')

    df, record = getDataFromCsv()
    print('')
    print('str(record)[:200] =', str(record)[:200])

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
    print('\n### test_3() #############################################################################################')

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


def test_readtable_and_update():
    db_name = movies_or_tv = 'test_movies'  # 'tv' #
    db_table = 'test_movie'

    db = setupDatabase(db_name, db_table)
    db_connection = db.getConnection()

    # test querying database
    print('\n### test querying database')
    a_dict_list = readTableAll(db_connection=db_connection, table_name=db_table, close_connection_afterward=False)
    print(f'\ntype(a_dict_list) = \n\t{type(a_dict_list)};')
    print(f'type(a_dict_list[0]) = \n\t{type(a_dict_list[0])}')
    print(f'str(a_dict_list)[:300] = \n\t{str(a_dict_list)[:700]}\n')

    # test updating row in database
    print('\n### test updating database')
    new_scraped_rg_id = "7644ef5d-e023-4134-974c-88bf0e1149ee"
    new_scraped_overview = "In the tradition of “Ferris Bueller’s Day Off” comes this refreshing comedy about a rebellious prankster with a crafty mind and a heart of gold. Rascal. Joker. Dreamer. Genius... You've never met a college student quite like \"Rancho.\" From the moment he arrives at India's most prestigious university, Rancho's outlandish schemes turn the campus upside down—along with the lives of his two newfound best friends. Together, they make life miserable for \"Virus,\" the school’s uptight and heartless dean. But when Rancho catches the eye of the dean's sexy daughter, Virus sets his sights on flunking out the \"3 idiots\" once and for all."

    for a_dict in a_dict_list:
        # print('record =', record)
        id = a_dict.get('id')
        title = a_dict.get('title')
        updateRowById(db_connection=db_connection, table_name=db_table, 
                      eid=id, title=title, rg_id=new_scraped_rg_id, overview=new_scraped_overview, 
                      close_connection_afterward=False)
        
        print('\n### test updating database with wrong ID')
        id = '000'
        updateRowById(db_connection=db_connection, table_name=db_table, 
                      eid=id, title=title, rg_id=new_scraped_rg_id, overview=new_scraped_overview, 
                      close_connection_afterward=False)
        break


if __name__ == '__main__':

    print('\n### test_setupdatabase_and_insert() #############################################################################################')
    test_setupdatabase_and_insert()

    print('\n### test_readtable() #############################################################################################')
    test_readtable_and_update()
