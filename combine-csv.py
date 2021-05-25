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
import pandas as pd

def combine():
    #set working directory
    dir = os.path.join(os.getcwd(), 'reelgood-database')
    dir = os.path.join(dir, 'movies')

    os.chdir(dir)

    #find all csv files in the folder
    #use glob pattern matching -> extension = 'csv'
    #save result in list -> all_filenames
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    print(all_filenames)

    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    combine()