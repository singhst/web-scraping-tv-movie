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

    def getColumnsByColNames(self,
                             col_name: Iterable[str] = ['title', 'year'],
                             return_type: str = 'records') -> Iterable[dict]:
        """
        col_name: `Iterable[str]`; 'Title', 'Year', 'Type', 'Rating', 'IMDB Score', 'Reelgood Rating Score', 'Available On'
        
        Return
        ------
        `Iterable[dict]`, a `list of dict` in json format.

        e.g.

        [
            {'Title': 'Breaking Bad', 'Year': 2008}, 

            {'Title': 'Game of Thrones', 'Year': 2011},
            
            ...
        ]

        Remark
        ------
        `json.dumps(the_return_dict_list)` make return dict become JSON string.
        """

        list_of_dict_in_json_format = self.dataframe[col_name].to_dict(orient=return_type)        
        
        return list_of_dict_in_json_format


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
    a_list_of_dict = titles.getColumnsByColNames()
    print("len(a_list_of_dict):", len(a_list_of_dict))
    print("type(a_list_of_dict):", type(a_list_of_dict))
    print("str(a_list_of_dict):", str(a_list_of_dict)[:200])

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

        writeToFile(json.dumps(a_list_of_dict),
                    f"databaseCsv_getColumnsByColName_dict",
                    "json",
                    temp_save_path)

    save_dict()
