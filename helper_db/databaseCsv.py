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
        return self.dataframe[col_name].to_dict()


if __name__ == "__main__":
    movies_or_tv = "tv"
    # folder_path = "reelgood-database"

    titles = databaseCsv(
        movies_or_tv,
        # folder_path
    )
    print(titles.getDataFrame())

    print(titles.getColumnsByColName())
    print(len(titles.getColumnsByColName()))