from helper.translateToUrlPath import translateToUrlPath
from helper_db.databaseMysql.setupDatabase import setupDatabase
from helper_db.databaseMysql.createTable import createTable

db_name = movies_or_tv = 'movies' # 'tv' #
db = setupDatabase(db_name)
db_connection = db.getConnection()

createTable(db_connection, 'movie')