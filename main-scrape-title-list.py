#!/usr/bin/env python
"""
Function,
Extract all TV Shows and Movies tables in Reelgood.com.

#########################
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
# import getopt
import urllib.request
from bs4 import BeautifulSoup
import selenium
import pandas as pd

from helper.folderHandler import folderCreate
from helper.getCmlArg import getCmlArg


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

        self.url_with_path = f'{url_domain}/{url_path}'

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

        print("self.url_with_path =", self.url_with_path)

        while 1:
            offset = f'?offset={self.offset_value}'
            url_with_path_query_string = self.url_with_path + offset
            df = self.getTableData(url_with_path_query_string)   #scrape a table data of movies/TV shows
            self.extracted_table.append(df)
            self.frames.append(df)

            print("self.offset_value =", self.offset_value)
            # print('df.iloc[[0]] =', df.iloc[[0]])

            # If all titles of movie/TV show are extracted
            # concat the df list and export to .csv
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


def main():

    # Get argument from command line
    url_path, folder_name = getCmlArg()
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
