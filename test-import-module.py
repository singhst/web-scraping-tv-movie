from helper.translateToUrlPath import translateToUrlPath
from helper_db.databaseMysql.setupDatabase import setupDatabase
from helper_db.databaseMysql.createTable import createTable
from helper_db.databaseMysql.insert import insert_a_row, insert_n_rows


db_name = movies_or_tv = 'movies' # 'tv' #
db_table = 'movie'

db = setupDatabase(db_name)
db_connection = db.getConnection()

createTable(db_connection, table_name=db_table)

# 55a2e378-dfb0-4473-b105-7478bb1dcfc1
# Se7en,
# 1995,
# 18+,
# 8.6/10,
# 100/100,
# + Rent or Buy
insert_a_row(db_connection, 
             table_name=db_table, 
             rg_id= '4355a2e378-dfb0-4473-b105-7478bb1dcfc1',
             title='Se7en', 
             year='1995', 
             rating='18+',
             imdb_score='8.6/10',
             reelgood_rating_score='100/100')


insert_n_rows(db_connection,
              table_name=db_table,
              rg_id='355a2e378-dfb0-4473-b105-7478bb1dcfc1',
              title='Se7en',
              year='1995',
              rating='18+',
              imdb_score='8.6/10',
              reelgood_rating_score='100/100')
