from typing import Iterable
import pandas as pd


class databaseCsv():

    def __init__(self,
                 movies_or_tv: str,
                 folder_path: str = "reelgood-database"
                 ):
        
        self.movies_or_tv = movies_or_tv
        self.folder_path = folder_path
        self.file_path = f"{self.folder_path}/all-{self.movies_or_tv}.csv"
        self.dataframe = pd.DataFrame
        self.importCsv()

    def importCsv(self):
        self.dataframe = pd.read_csv(self.file_path)

    def getDataFrame(self) -> pd.DataFrame:
        return self.dataframe

    def getColumnsByColName(self, col_name: Iterable[str] = ['Title', 'Year']) -> dict:
        """
        col_name: `str`; 'Title', 'Year', 'Type', 'Rating', 'IMDB Score', 'Reelgood Rating Score', 'Available On'
        """
        return self.dataframe[col_name].to_dict('list')


if __name__ == "__main__":
    movies_or_tv = "tv"
    # folder_path = "reelgood-database"

    titles = databaseCsv(
        movies_or_tv,
        # folder_path
    )

    #########################################
    print(titles.getDataFrame())


    #########################################
    a_dict = titles.getColumnsByColName()
    print(str(a_dict)[:200])

    # The below use to change path
    import os, sys
    currentdir = os.path.dirname(os.path.realpath(__file__))
    parentdir = os.path.dirname(currentdir)
    sys.path.append(parentdir)
    ## Import the lib under new path
    from helper.folderHandler import folderCreate
    from helper.writeToFile import writeToFile

    # Create folders to save scraped data
    current_path = os.getcwd()
    path = os.path.join(current_path, 'test')
    temp_save_path = folderCreate(path, 'temp_save')

    import json
    writeToFile(json.dumps(a_dict),
                f"databaseCsv_getColumnsByColName_dict",
                "json",
                temp_save_path)


    #########################################
    print(len(titles.getColumnsByColName()))
