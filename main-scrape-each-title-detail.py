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
    path = os.path.join(current_path, 'reelgood-database')

    

    


if __name__ == "__main__":
    
    get_movie_or_tv = 'movies'   #'tv'

    main(get_movie_or_tv)
