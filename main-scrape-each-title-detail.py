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

from helper.translateToUrlPath import translateToUrlPath
# from helper.getCmlArg import getCmlArg
# from helper.tempStorage import tempStorage
from helper.folderHandler import folderCreate
from helper.writeToFile import writeToFile
from helper_db.databaseCsv import databaseCsv
from helper_scraping.webScrapeEachTitleDetail import webScrapeEachTitleDetail


def main(get_movie_or_tv: str = 'movies'):
    # Create folders to save scraped data
    current_path = os.getcwd()
    folder_path = f'reelgood-database/{get_movie_or_tv}'
    path = os.path.join(current_path, folder_path)
    print(path)
    
    save_path = folderCreate(path, 'json')

    # Get title list and year list from database
    database = databaseCsv('movies', os.path.join(os.getcwd(), 'reelgood-database'))
    db_table_dict_list = database.getColumnsByColNames()
    print(str(db_table_dict_list)[:400])

    # title_list = [a_dict.get('Title') for a_dict in db_table_dict_list]
    # year_list = [a_dict.get('Year') for a_dict in db_table_dict_list]

    # Scrape detail info of each movie / TV show 
    scraper = webScrapeEachTitleDetail()
    url_domain = 'https://reelgood.com/'
    movie_or_show = 'movie'

    for i, a_dict in zip(range(len(db_table_dict_list)), db_table_dict_list):
        title = a_dict.get('Title')
        year = a_dict.get('Year')

        # Remove title's symbols ==> keep only letter, number and space char
        title_no_symbol = re.sub(r'[^a-zA-Z0-9 ]+', '', title)
        title_no_symbol = title_no_symbol.replace(' ', '_')

        scraper.setUrl(movie_or_show, title, year, url_domain)

        #scrape each movie/tv show html page
        scraper.scrapeHtmlPageSelenium()
        scraper.extractTitleDetail()

        # Get .js json from <script type='text/javascript'> tag 
        # This json contains all information about the movie/tv show
        meta_data = scraper.getMetaData()
        str_meta_data = json.dumps(meta_data)
        writeToFile(str_meta_data,
                    f"{i}_{title_no_symbol}_{year}_1_meta", 
                    "json", 
                    save_path)


if __name__ == "__main__":
    
    get_movie_or_tv = 'movies'   #'tv'

    main(get_movie_or_tv)
