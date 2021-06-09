from typing import Iterable
import pandas as pd
import json


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

    def getColumnsByColName(self, 
                            col_name: Iterable[str] = ['Title', 'Year'],
                            return_type: str = 'table') -> dict:
        """
        col_name: `str`; 'Title', 'Year', 'Type', 'Rating', 'IMDB Score', 'Reelgood Rating Score', 'Available On'
        """

        json_str_unformated = self.dataframe[col_name].to_json(orient=return_type)
        a_dict_in_json_format = json.loads(json_str_unformated)
        
        return a_dict_in_json_format


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
    print(type(a_dict))
    print(str(a_dict)[:200])

    def save_dict():
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

        writeToFile(json.dumps(a_dict),
                    f"databaseCsv_getColumnsByColName_dict",
                    "json",
                    temp_save_path)

    save_dict()


    #########################################
    print(len(titles.getColumnsByColName()))
