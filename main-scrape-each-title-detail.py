"""
Function,
Extract detail information of each Movie / TV show by reading the scraped movie/tv show title table.

#########################
routing pattern,

domain:     https://reelgood.com
tv shows:   /show
movie:      /movie
"""


import os, sys
import json
import re
from typing import Iterable

# Helper
from helper.folderHandler import folderCreate
from helper.writeToFile import writeToFile
from helper_scraping.webScrapeEachTitleDetail import webScrapeEachTitleDetail

# Database
from helper_db.databaseCsv import databaseCsv
from helper_db.databaseMysql.setupDatabase import setupDatabase
from helper_db.databaseMysql.readTable import readTableAll
from helper_db.databaseMysql.update import updateRowById
from helper_db.databaseMysql.insert import insertNRowsToDb


def getTitleListCsv() -> Iterable[dict]:
    """"Get movie/tv show title list from .csv"""
    db_movie = databaseCsv('movies', os.path.join(os.getcwd(), 'reelgood-database'))
    db_table_movie_row = db_movie.getColumnsByColNames(col_name=['title','year'])
    print('> str(db_table_movie_row)[:400] =', str(db_table_movie_row)[:400])

    return db_table_movie_row


def getTitleListMysql(db_connection, db_table_name) -> Iterable[dict]:
    """"Get movie/tv show title list from mysql server."""
    db_table_movie_row = readTableAll(db_connection=db_connection, table_name=db_table_name, close_connection_afterward=False)
    print('> str(db_table_movie_row)[:400] =', str(db_table_movie_row)[:400])
    
    return db_table_movie_row


def main(get_movies_or_tv: str = 'movies'):
    # Create folders to save scraped data
    current_path = os.getcwd()
    folder_path = f'reelgood-database/{get_movies_or_tv}'
    path = os.path.join(current_path, folder_path)
    print(path)
    
    save_path = folderCreate(path, 'json')


    # Get title list and year list from `movie` table in `movies` database
    print('\n=== Reading data... =========================================')
    # (1) read from .csv
    db_table_movie_row = getTitleListCsv()
    # (2) read from MySQL
    table_name_movie = get_movies_or_tv.replace('s', '')   #'movie' instead of 'movies'
    db_movie = setupDatabase(db_name=get_movies_or_tv, db_table_name=table_name_movie)
    db_connection_movie = db_movie.getConnection()
    db_table_movie_row = getTitleListMysql(db_connection_movie, table_name_movie)


    # Connect to `availability` table in `movies` database
    print('\n=== Setting... =========================================')
    table_name_availability = 'availability'   #'movie' instead of 'movies'
    db_availability = setupDatabase(db_name=get_movies_or_tv, db_table_name=table_name_availability)
    db_connection_availability = db_availability.getConnection()


    print('\n=== Scraping ... =========================================')
    # Scrape detail info of each movie / TV show 
    scraper = webScrapeEachTitleDetail()
    url_domain = 'https://reelgood.com'
    movie_or_show = get_movies_or_tv.replace('s', '')

    for i, a_dict in zip(range(1, len(db_table_movie_row)+1), db_table_movie_row):
        print()
        print(f'> {i}th {movie_or_show}')
        # print('\ta_dict =', a_dict)
        title = a_dict.get('title')
        year = a_dict.get('year')

        scraper.setUrl(movie_or_show=movie_or_show, title=title, year=year, url_domain=url_domain)

        # Scrape each movie/tv show html page
        # and Check whether the info of this movie/tv show exist or not
        if not scraper.scrapeHtmlPageSelenium():
            print(f"> `('{title}', '{year}')` not found!")
        else:
            scraper.extractTitleDetail()

            # Get and store the meta data in JSON first
            ## Get .js json from <script type='text/javascript'> tag 
            ## This json contains all information about the movie/tv show
            meta_data = scraper.getMetaData()
            str_meta_data = json.dumps(meta_data)
            ## Remove title's symbols ==> keep only letter, number and space char
            title_no_symbol = re.sub(r'[^a-zA-Z0-9 ]+', '', title)
            title_no_symbol = title_no_symbol.replace(' ', '_')
            writeToFile(str_meta_data,
                        f"meta_{scraper.url_slug}", 
                        "json", 
                        save_path)

            # Extract info from meta data
            title = scraper.title
            year = scraper.year
            rg_id = scraper.rg_id
            overview = scraper.overview
            source_links = scraper.source_links
            _source_links_dict_list = scraper._source_links_dict_list
            source_name = ''
            source_movie_id = ''
            print(f'> _source_links_dict_list={_source_links_dict_list}')
            print(f'> title={title}')
            print(f'> rg_id={rg_id}')
            print(f'> overview={overview[:10]}')
            print(f'> str(source_links)[:100]={str(source_links)[:100]}')
            

            # Update the row in `movie` table in MySQL server by `id` 
            updateRowById(db_connection=db_connection_movie, table_name=table_name_movie, 
                          eid=i, title=title, year=year, rg_id=rg_id, overview=overview,
                          close_connection_afterward=False)
            ## Insert links to `availability` table
            print(f'> {len(source_links)} streaming links are inserting to DB...')
            for link in source_links:
                record = [(rg_id, source_name, source_movie_id, link)]
                added_row_count = insertNRowsToDb(db_connection=db_connection_availability,
                                                  table_name=table_name_availability,
                                                  record=record,
                                                  close_connection_afterward=False
                                                  )


if __name__ == "__main__":
    
    get_movies_or_tv = 'movies'   #'tv'

    main(get_movies_or_tv)
