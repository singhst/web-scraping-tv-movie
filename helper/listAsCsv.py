import pandas as pd

class listAsCsv():

    def __init__(self,
                 movies_or_tv: str,
                 folder_path: str = "/reelgood-database"
                 ):
        
        self.movies_or_tv = movies_or_tv
        self.folder_path = folder_path
        self.file_path = f"{self.folder_path}/all-{self.movies_or_tv}.csv"
        self.dataframe = pd.DataFrame
        self.importCsv()

    def importCsv(self):
        self.dataframe = pd.read_csv(self.file_path)


if __name__ == "__main__":
    movies_or_tv = "tv"
    folder_path = "reelgood-database"

    titleList = listAsCsv(movies_or_tv, folder_path)
    print(titleList.dataframe)