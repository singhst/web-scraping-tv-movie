#!/usr/bin/env python
"""Extract TV Shows and Movies in Reelgood.com.

    * get_spreadsheet_cols - returns the column headers of the file
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
import sys, getopt
import urllib
from bs4 import BeautifulSoup
import selenium
import pandas as pd


class webScraping:

    def __init__(self,
                 class_of_table: str,
                 url_domain: str,
                 url_path: str,
                 csv_export_path: str) -> None:

        self.class_of_table = class_of_table
        self.csv_export_path = csv_export_path
        self.url_path = url_path
        self.url_domain = url_domain

        self.url = f'{url_domain}/{url_path}'

        self.frames = []
        self.return_df = []
        self.offset_value = 0
        self.old_offset_value = 0

        pass


    def getTableData(self) -> pd.DataFrame:
        """Gets table data from the web. Return the extracted table as `pandas` `dataframe`.

        Parameters
        ----------
        self.url : str
            The self.url of the website
        class_of_table : str

        Returns
        -------
        pd.Dataframe
            `dataframe` of names of TV Shows or Movies.
        None
            Return `None` if no data can be extracted.
        """

        # add User-Agent to header to pretend as browser visit, more detials can be found in FireBug plugin
        # if we don't add the below, error message occurs. ERROR: urllib.error.HTTPError: HTTP Error 403: Forbidden
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=self.url, headers=headers)

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


    def getAllTables(self) -> pd.DataFrame:

        df = pd.DataFrame()

        print("self.url =", self.url)

        while df is not None:
            offset = f'?offset={self.offset_value}'
            self.url += offset
            df = self.getTableData()
            self.return_df.append(df)
            self.frames.append(df)

            if (self.offset_value % 2500) == 0 & self.offset_value > 0:
                concat_frames = pd.concat(self.frames)

                csvname = f'{self.url_path}-offset-{self.old_offset_value}-to-{self.offset_value}.csv'
                concat_frames.to_csv(self.csv_export_path+'/'+csvname)

                # print(f'self.old_offset_value={self.old_offset_value}, self.offset={self.offset_value}')
                print("concat_frames.shape =", concat_frames.shape)
                print("> export: ", self.csv_export_path+'\\'+csvname)

                self.old_offset_value = self.offset_value
                self.frames = []

            self.offset_value += 50

        print()
        print(f'end offset={self.offset_value}, end df.shape={df.shape}')
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
    """Get the arguments from command line. Return `str` 'tv' or 'movies'
    """
    # print("argv =", argv)

    url_path = ''
    
    if not argv:
        print('> Please enter arg, `main.py -h OR -t OR -m`')
        sys.exit(2)

    try:
        argumentList = argv
        shortopts = "htvm"     
        long_options = ["tv", "movie"]
        opts, args = getopt.getopt(argumentList, shortopts, long_options)

    except getopt.GetoptError:
        print('> Wrong arg, `test.py -h OR -t OR -m`')
        sys.exit(2)

    # print("opts =", opts)

    for opt, arg in opts:
        if opt == '-h':
            print('> in `-h`, `test.py -t OR -m`')
            sys.exit()
        elif opt in ("-t", "-tv", "-tvshow", "-tvshows"):
            url_path = 'tv'
        elif opt in ("-m", "-movie", "-movies"):
            url_path = 'movies'
    # print('url path is "', url_path)

    return url_path


def main():

    # Get argument from command line
    url_path = getCmlArg(sys.argv[1:])
    print("url_path =", url_path)

    # init needed variables
    current_path = os.getcwd()
    path = os.path.join(current_path, 'reelgood-database')

    class_of_table = 'css-1179hly'
    url_domain = 'https://reelgood.com'

    # Get TV show or Movie data
    csv_export_path = folderCreate(path, url_path)

    tvScrapper = webScraping(class_of_table, url_domain,
                             url_path, csv_export_path)
    df = tvScrapper.getAllTables()
    # print("df=",df)
    # print("df.shape=",df.shape)


if __name__ == "__main__":
    main()
