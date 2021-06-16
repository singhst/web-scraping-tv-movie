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


def main(get_movies_or_tv: str = 'movies'):
    # Create folders to save scraped data
    current_path = os.getcwd()
    folder_path = f'reelgood-database/{get_movies_or_tv}'
    path = os.path.join(current_path, folder_path)
    print(path)
    
    save_path = folderCreate(path, 'json')


    # Get title list and year list from database
    database = databaseCsv('movies', os.path.join(os.getcwd(), 'reelgood-database'))
    db_table_dict_list = database.getColumnsByColNames()
    print(str(db_table_dict_list)[:400])
    

    # Scrape detail info of each movie / TV show 
    scraper = webScrapeEachTitleDetail()
    url_domain = 'https://reelgood.com'
    movie_or_show = get_movies_or_tv.replace('s', '')

    for i, a_dict in zip(range(len(db_table_dict_list)), db_table_dict_list):
        title = a_dict.get('Title')
        year = a_dict.get('Year')

        scraper.setUrl(movie_or_show=movie_or_show, title=title, year=year, url_domain=url_domain)

        # Scrape each movie/tv show html page
        # and Check whether the info of this movie/tv show exist or not
        if not scraper.scrapeHtmlPageSelenium():
            print(f"> `('{title}', '{year}')` not found!")
        else:
            scraper.extractTitleDetail()

            # Get .js json from <script type='text/javascript'> tag 
            # This json contains all information about the movie/tv show
            meta_data = scraper.getMetaData()
            str_meta_data = json.dumps(meta_data)

            # Remove title's symbols ==> keep only letter, number and space char
            title_no_symbol = re.sub(r'[^a-zA-Z0-9 ]+', '', title)
            title_no_symbol = title_no_symbol.replace(' ', '_')
            writeToFile(str_meta_data,
                        f"meta_{i}_{title_no_symbol}_{year}", 
                        "json", 
                        save_path)


if __name__ == "__main__":
    
    get_movies_or_tv = 'movies'   #'tv'

    main(get_movies_or_tv)
