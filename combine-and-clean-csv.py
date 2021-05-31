# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 06:56:16 2019
@author: Chris

https://github.com/ekapope/Combine-CSV-files-in-the-folder/blob/master/Combine_CSVs.py
"""
#credited:
#https://stackoverflow.com/questions/9234560/find-all-csv-files-in-a-directory-using-python/12280052

import os
import glob
from datetime import date
import pandas as pd


folder_name = 'tv'
# folder_name = 'movies'

movie_or_tv = folder_name
parent_folder = 'reelgood-database'
backup_folder = '(backup)'


def cleanDf(df: pd.DataFrame):
    """
    The following are the instructions of the cleansing process:
    1. `7th` column                     ==> `IMDB Score` as column name
    2. `8th` column                     ==> `Reelgood Rating Score` as column name
    3. `1st`, `11th` column             ==> Remove, useless
    4. `2nd`, `4th` & `10th` columns    ==> Remove, empty columns
    """

    # df.columns.values[6] = 'IMDB Score'
    df = df.rename(columns={df.columns[6]: 'IMDB Score'})
    
    # df.columns.values[7] = 'Reelgood Rating Score'
    df = df.rename(columns={df.columns[7]: 'Reelgood Rating Score'})
    
    df.drop(df.columns[[0,10]], axis=1, inplace=True)

    df.replace("", float("NaN"), inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    
    return df


def combineCsv():
    #set working directory
    dir = os.path.join(os.getcwd(), parent_folder)
    dir = os.path.join(dir, folder_name)

    os.chdir(dir)

    #find all csv files in the folder
    #use glob pattern matching -> extension = 'csv'
    #save result in list -> all_filenames
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    print(all_filenames)

    #combine all files in the list
    combined_csv = pd.concat([cleanDf(pd.read_csv(f)) for f in all_filenames])
    
    #export to csv
    os.chdir("..")   #change dir to parent folder `/reelgood-database`
    dir = os.getcwd()
    file_name = f"all-{movie_or_tv}.csv"
    combined_csv.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"> export '{dir}/{file_name}'")
    
    dir = os.path.join(dir, backup_folder)  #change dir to folder `/reelgood-database/(backup)`
    os.chdir(dir)
    dir = os.getcwd()
    today = date.today()
    file_name = f"all-{movie_or_tv}-{today}.csv"
    combined_csv.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"> export '{os.getcwd()}/{file_name}'")

    return combined_csv


def test():
    #set working directory
    dir = os.path.join(os.getcwd(), 'reelgood-database')
    dir = os.path.join(dir, folder_name)

    os.chdir(dir)

    #find all csv files in the folder
    #use glob pattern matching -> extension = 'csv'
    #save result in list -> all_filenames
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    print(all_filenames[0])

    df = pd.read_csv(all_filenames[0])
    print(df.head())

    df = cleanDf(df)
    print(df.head())


if __name__ == "__main__":
    
    # test()
    df = combineCsv()
    print(df.head())
    print(df.shape)