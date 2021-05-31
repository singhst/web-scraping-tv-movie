#!/usr/bin/env python
"""Extract TV Shows and Movies in Reelgood.com.

    * main - the main function of the script

    https://reelgood.com
    /tv
    /genre
    /crime
    ?filter-imdb_end=6.9&filter-imdb_start=4
    &filter-rg_end=70&filter-rg_start=30
    &filter-year_end=2018&filter-year_start=1998
"""

import os
import sys
from datetime import date
import getopt
import urllib
from bs4 import BeautifulSoup
import selenium
import pandas as pd


class webScrapeTitleList:

    def __init__(self,
                 class_of_table: str,
                 csv_export_path: str,
                 folder_name: str,
                 url_domain: str,
                 url_path: str) -> None:

        self.class_of_table = class_of_table
        self.csv_export_path = csv_export_path
        self.folder_name = folder_name
        self.url_domain = url_domain
        self.url_path = url_path

        self.url = f'{url_domain}/{url_path}'

        self.offset_value = 0
        self.old_offset_value = 0

        self.frames = []
        self.extracted_table = []

        pass

    def getTableData(self, url) -> pd.DataFrame:
        """Gets table data from the web. Return the extracted table as `pandas` `dataframe`.

        Parameters
        ----------
        url : str
            The url of the website, e.g. `https://reelgood.com/movies?offset=50`
        class_of_table : str

        Returns
        -------
        pd.Dataframe
            `dataframe` of names of TV Shows or Movies.
        None
            Return `None` if no data can be extracted.
        """

        # print("url =", url)

        # add User-Agent to header to pretend as browser visit, more detials can be found in FireBug plugin
        # if we don't add the below, error message occurs. ERROR: urllib.error.HTTPError: HTTP Error 403: Forbidden
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=url, headers=headers)

        try:
            html = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')

            table = soup.find('table', {'class': self.class_of_table})
            columns = [th.text.replace('\n', '')
                       for th in table.find('tr').find_all('th')]
            # print(columns)

            trs = table.find_all('tr')[1:]
            rows = list()
            for tr in trs:
                rows.append([td.text.replace('\n', '').replace('\xa0', '')
                             for td in tr.find_all('td')])

            df = pd.DataFrame(data=rows, columns=columns)
            return df

        except:
            return None

    def combineAndExportDataFrame(self):
        concat_frames = pd.concat(self.frames)
        
        today = date.today()
        csvname = f'{today}-{self.folder_name}-offset-{self.old_offset_value}-to-{self.offset_value}.csv'
        concat_frames.to_csv(self.csv_export_path+'/'+csvname)

        # print(f'self.old_offset_value={self.old_offset_value}, self.offset={self.offset_value}')
        print("concat_frames.shape =", concat_frames.shape)
        print("> export: ", self.csv_export_path+'\\'+csvname)

        self.old_offset_value = self.offset_value
        self.frames = []

        return

    def getAllTables(self):

        df = pd.DataFrame()

        print("self.url =", self.url)

        while 1:
            offset = f'?offset={self.offset_value}'
            url_with_path = self.url + offset
            df = self.getTableData(url_with_path)
            self.extracted_table.append(df)
            self.frames.append(df)

            print("self.offset_value =", self.offset_value)
            # print('df.iloc[[0]] =', df.iloc[[0]])

            if df is None:
                self.combineAndExportDataFrame()
                print()
                print(f'end offset={self.offset_value}, len(self.extracted_table)={len(self.extracted_table)}')
                print(f'type(self.extracted_table[-1])={type(self.extracted_table[-1])}')
                print(f'self.extracted_table[-1]={self.extracted_table[-1]}')
                return

            if (self.offset_value % (10000) == 0) and (self.offset_value > 0):
                # if (self.offset_value % 50) == 0:
                self.combineAndExportDataFrame()

            self.offset_value += 50

        return


def folderExist(path: str) -> bool:
    """Check the folder exists or not
    """
    # print('os.path.exists(path)=',os.path.exists(path))
    return os.path.exists(path)


def folderCreate(path: str,
                 foldername: str = ''):
    """
    https://www.geeksforgeeks.org/create-a-directory-in-python/
    """
    path = os.path.join(path, foldername)

    if not folderExist(path):
        os.makedirs(path)
        print(f"> creates {path}")
    else:
        print(f"> folder existed, {path}")

    return path


def getCmlArg(argv) -> str:
    """Get the arguments from command line. Return `str` 'tv' / 'curated/trending-picks' or 'movies' . 'curated/trending-movies'
    """
    # print("argv =", argv)

    if not argv:
        print('> Please enter arg, `test.py -h OR -t OR -m <trend> (optional)`')
        sys.exit(2)

    try:
        argumentList = argv
        shortopts = "htm"
        long_options = ["tv", "movie"]
        opts, args = getopt.getopt(argumentList, shortopts, long_options)

    except getopt.GetoptError:
        print('> Wrong arg, `test.py -h OR -t OR -m <trend> (optional)`')
        sys.exit(2)

    # print("opts =", opts)
    # print("args =", args)

    # for opt, arg in opts:
    opt = opts[0][0]
    if opt == '-h':
        print('> in `-h`, `test.py -h OR -t OR -m <trend> (optional)`')
        sys.exit()
    elif opt in ("-t", "-tv", "-tvshow", "-tvshows"):
        try:
            if args[0] in ["trend", "trending"]:
                return 'curated/trending-picks', 'trending-tv'
        except:
            return 'tv', 'tv'
    elif opt in ("-m", "-movie", "-movies"):
        try:
            if args[0] in ["trend", "trending"]:
                return 'curated/trending-movies', 'trending-movies'
        except:
            return 'movies', 'movies'
    # print('url path is "', url_path)

    print('> wrong argument, `test.py -h OR -t OR -m <trend> (optional)`')
    sys.exit()


def main():

    # Get argument from command line
    url_path, folder_name = getCmlArg(sys.argv[1:])
    print("url_path =", url_path)

    # init needed variables
    current_path = os.getcwd()
    path = os.path.join(current_path, 'reelgood-database')

    class_of_table = 'css-1179hly'
    url_domain = 'https://reelgood.com'

    # Get TV show or Movie data
    csv_export_path = folderCreate(path, folder_name)

    scrapper = webScrapeTitleList(class_of_table,
                           csv_export_path=csv_export_path,
                           folder_name=folder_name,
                           url_domain=url_domain,
                           url_path=url_path)
    scrapper.getAllTables()
    print(len(scrapper.extracted_table))
    # print("df=",df)
    # print("df.shape=",df.shape)


if __name__ == "__main__":
    main()
