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

from helper.getCmlArg import getCmlArg
from helper.folderHandler import folderCreate
from helper_db.databaseMysql.setupDatabase import setupDatabase
from helper_db.databaseMysql.insert import insertPandasDfToDb


import os
import sys
from datetime import date
# import getopt
import urllib.request
from bs4 import BeautifulSoup
import selenium
import pandas as pd
pd.set_option("display.max_columns", None)


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

        # store df temporarily, it is cleared every (offset_value % 10,000 == 0)
        self.temp_frames = []
        # stored all df into one list, e.g. `[df1, df2, ..., df_n]`
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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
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

    def cleanDf(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        The following are the instructions of the cleansing process:
        1. `6th` column                     ==> `IMDB Score` as column name
        2. `7th` column                     ==> `Reelgood Rating Score` as column name
        """

        df.columns.values[5] = 'IMDB Score'
        # df.rename(columns={df.columns[5]: 'IMDB Score'}, inplace=True)

        df.columns.values[6] = 'Reelgood Rating Score'
        # df.rename(columns={df.columns[6]: 'Reelgood Rating Score'}, inplace=True)

        # drop columns with `''` `empty str` column header
        df.drop([''], axis=1, inplace=True)
        # fill `''` `empty str` cell values to nan
        df.replace("", float("NaN"), inplace=True)
        # drop columns with nan as column value
        df.dropna(how='all', axis=1, inplace=True)

        return df

    def combineAndExportDataframe(self):
        concat_frames = pd.concat(self.temp_frames)

        today = date.today()
        csvname = f'{today}-{self.folder_name}-offset-{self.old_offset_value}-to-{self.offset_value}.csv'
        path = os.path.join(self.csv_export_path, csvname)

        concat_frames.to_csv(path)

        # print(f'self.old_offset_value={self.old_offset_value}, self.offset={self.offset_value}')
        print("concat_frames.shape =", concat_frames.shape)
        print("> export: ", path)

        self.old_offset_value = self.offset_value
        self.temp_frames = []

        return

    def exportTableDataToMysql(self, df: pd.DataFrame):
        db = setupDatabase(db_name=self.folder_name, db_table_name='movie')
        db_connection = db.getConnection()
        df.insert(0, 'rg_id', '')
        df.insert(3, 'overview', '')
        df = df.iloc[:, 0:-1] #remove last column 'Available On'; get all rows, 1st col to (last - 1) col
        insertPandasDfToDb(db_connection=db_connection, table_name='movie', df=df)


    def getAllTables(self):

        df = pd.DataFrame()

        print("self.url_with_path =", self.url_with_path)

        while 1:
            print("self.offset_value =", self.offset_value)

            offset = f'?offset={self.offset_value}'
            url_with_path_query_string = self.url_with_path + offset
            # scrape a table data of movies/TV shows
            df = self.getTableData(url_with_path_query_string)

            # If all titles of movie/TV show are extracted ==> web returns None
            # then concat the df list and export to .csv
            if df is None:
                self.combineAndExportDataframe()
                self.exportAllDataframeToCsv()
                print()
                print(f'> end offset={self.offset_value}, len(self.extracted_table)={len(self.extracted_table)}')
                print(f'type(self.extracted_table[-1])={type(self.extracted_table[-1])}')
                print(f'self.extracted_table[-1]=\n{self.extracted_table[-1].head(5)}')
                return

            # save and export title list every 10,000 offset_value,
            # avoid losing all scraped data if errors occur
            if (self.offset_value % (10000) == 0) and (self.offset_value > 0):
                # if (self.offset_value % 50) == 0:
                self.combineAndExportDataframe()

            print('> original df title =', list(df.columns))
            df = self.cleanDf(df)
            print('> cleaned df title =', list(df.columns))

            self.extracted_table.append(df)
            self.temp_frames.append(df)
            
            # self.exportTableDataToMysql(df)

            self.offset_value += 50

        return

    def exportAllDataframeToCsv(self):
        concat_frames = pd.concat(self.extracted_table)

        today = date.today()
        csvname = f'{today}-all-{self.folder_name}.csv'
        path = os.path.join(self.csv_export_path, csvname)
        concat_frames.to_csv(path)

        # print(f'self.old_offset_value={self.old_offset_value}, self.offset={self.offset_value}')
        print("concat_frames.shape =", concat_frames.shape)
        print("> export: ", path)


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
