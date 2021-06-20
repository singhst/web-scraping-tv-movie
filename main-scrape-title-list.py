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
from mysql.connector import Error as mysqlError


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
                 url_path: str,
                 start_offset_value:int=0) -> None:

        self.class_of_table = class_of_table
        self.csv_export_path = csv_export_path
        self.folder_name = folder_name
        self.url_domain = url_domain
        self.url_path = url_path

        self.url_with_path = f'{url_domain}/{url_path}'

        self.url_offset_value = start_offset_value
        self.old_offset_value = start_offset_value

        # store df temporarily, it is cleared every (url_offset_value % 10,000 == 0)
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
        3. `last` column                    ==> `url_offset_value` as column name, new
        """

        df.columns.values[5] = 'IMDB Score'
        # df.rename(columns={df.columns[5]: 'IMDB Score'}, inplace=True)

        df.columns.values[6] = 'Reelgood Rating Score'
        # df.rename(columns={df.columns[6]: 'Reelgood Rating Score'}, inplace=True)

        # drop columns with `''` `empty str` column header
        df.drop([''], axis=1, inplace=True)
        # fill `''` `empty str` cell values to nan
        df.replace('', float('NaN'), inplace=True)
        # drop columns with nan as column value
        df.dropna(how='all', axis=1, inplace=True)
        # Some title name is '', mysql cannot accept `nan` but accept `''` empty string
        # ==> fill `float("NaN")` `nan` cell values to ''
        df.replace(float('NaN'), '', inplace=True)

        df['url_offset_value'] = str(self.url_offset_value)

        return df

    def combineAndExportDataframe(self):
        concat_frames = pd.concat(self.temp_frames)

        today = date.today()
        csvname = f'{today}-{self.folder_name}-offset-{self.old_offset_value}-to-{self.url_offset_value}.csv'
        path = os.path.join(self.csv_export_path, csvname)

        concat_frames.to_csv(path, index=False)

        # print(f'self.old_offset_value={self.old_offset_value}, self.offset={self.url_offset_value}')
        print("concat_frames.shape =", concat_frames.shape)
        print("> export: ", path)

        self.old_offset_value = self.url_offset_value
        self.temp_frames = []

        return

    def exportTableDataToMysql(self, df: pd.DataFrame):
        try:
            db = setupDatabase(db_name=self.folder_name, db_table_name='movie')
            db_connection = db.getConnection()
            df.insert(0, 'rg_id', '')
            df.insert(3, 'overview', '')
            #remove last column 'Available On'
            # df = df.iloc[:, 0:-1] #get all rows, 1st col to (last - 1) col
            df = df.loc[:, df.columns != 'Available On']
            insertPandasDfToDb(db_connection=db_connection, table_name='movie', df=df)
            
        except(Exception, mysqlError) as error:
            print(f'\n\t==> Fail.')
            print(f'\t> Error = `{error}`')

            today = date.today()
            csvname = f'{today}-{self.folder_name}-mysql-error-offset-{self.url_offset_value}.csv'
            path = os.path.join(self.csv_export_path, csvname)
            df.to_csv(path, index=False)

            print("\tdf.shape =", df.shape)
            print("\t> export: ", path, '\n\n')


    def getAllTables(self):

        df = pd.DataFrame()

        print("self.url_with_path =", self.url_with_path)

        while 1:
            print()
            print("self.url_offset_value =", self.url_offset_value)

            offset = f'?offset={self.url_offset_value}'
            url_with_path_query_string = self.url_with_path + offset
            # scrape a table data of movies/TV shows
            df = self.getTableData(url_with_path_query_string)

            # If all titles of movie/TV show are extracted ==> web returns None
            # then concat the df list and export to .csv
            if df is None:
                print()
                print(f'> end offset={self.url_offset_value}, len(self.extracted_table)={len(self.extracted_table)}')
                print(f'type(self.extracted_table[-1])={type(self.extracted_table[-1])}')
                print(f'self.extracted_table[-1]=\n{self.extracted_table[-1].head(5)}')
                print()
                self.combineAndExportDataframe()
                self.exportAllDataframe()
                return

            # save and export title list every 10,000 url_offset_value,
            # avoid losing all scraped data if errors occur
            if (self.url_offset_value % (10000) == 0) and (self.url_offset_value > 0):
                # if (self.url_offset_value % 50) == 0:
                self.combineAndExportDataframe()

            print('> df.shape =', df.shape)
            print('> original df title =', list(df.columns))
            df = self.cleanDf(df)
            print('> cleaned df title =', list(df.columns))
            
            # self.exportTableDataToMysql(df)   #save 50 titles to mysql database every time

            # df['url_offset_value'] = str(self.url_offset_value)
            # print('> add url_offset_value col in df, title =', list(df.columns))

            self.extracted_table.append(df)
            self.temp_frames.append(df)

            self.url_offset_value += 50

        return

    def exportAllDataframe(self):
        concat_frames = pd.concat(self.extracted_table)

        today = date.today()
        csvname = f'{today}-all-{self.folder_name}.csv'
        path = os.path.join(self.csv_export_path, csvname)
        concat_frames.to_csv(path, index=False)
        self.exportTableDataToMysql(concat_frames)   #save all scraped titles to mysql database

        # print(f'self.old_offset_value={self.old_offset_value}, self.offset={self.url_offset_value}')
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
                                  url_path=url_path,
                                  start_offset_value=0  #int(70000)
                                  )
    scrapper.getAllTables()
    print(len(scrapper.extracted_table))
    # print("df=",df)
    # print("df.shape=",df.shape)


if __name__ == "__main__":
    main()
