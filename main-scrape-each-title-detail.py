from helper.translateToUrlPath import translateToUrlPath
from helper.listAsCsv import listAsCsv

from typing import Iterable
import requests
from bs4 import BeautifulSoup

"""
routing pattern,

domain:     https://reelgood.com
tv shows:   /show
movie:      /movie
"""


class webScrapeEachTitleDetail():

    def __init__(self,
                 url_domain: str,
                 movie_or_show: str,
                 title: str,
                 year: str):
        self.url_domain = url_domain        # https://reelgood.com
        self.url_path_var1 = movie_or_show  # /movie OR /show
        self.url_path_var2 = title          # /{title of movie or TV show}-{year}, space is replaced by hyphen `-`
        self.url_path_var3 = year           #

        self.url = translateToUrlPath(url_domain, movie_or_show, title, year)
        print(self.url)

        self.soup = ''
        self.getHtmlPage()

    def getHtmlPage(self) -> BeautifulSoup.new_tag:
        html_text = requests.get(self.url).text
        self.soup = BeautifulSoup(html_text, 'html.parser')

        writeToFile(html_text, "extracted_html_text", "html")
        writeToFile(self.soup, "extracted_html", "html")
        # print(type(self.soup))
        
        return

    def getDescription(self) -> str:
        p = self.soup.find('p', itemprop="description")
        for x in p:
            return str(x)
        return

    def getLink(self):
        pass


def writeToFile(content: Iterable[str],
                file_name: str = "extracted",
                file_type: str = "txt",
                file_path: str = "test"):

    if isinstance(content, list):
        if not isinstance(content[0], str):
            content = [str(c) for c in content]
    elif not isinstance(content, str):
        content = str(content)

    # Program to show various ways to read and
    # write data in a file.
    file1 = open(f"{file_path}/{file_name}.{file_type}", "w")

    file1.writelines(content)
    file1.close()  # to change file access modes


def test():
    url_domain = 'https://reelgood.com'
    movie_or_show = 'movie'
    title = "The Intouchables"
    year = "2011"

    scrapper = webScrapeEachTitleDetail(url_domain, movie_or_show, title, year)
    content = scrapper.getDescription()
    print(content)
    print(type(content))
    # writeTxt(content)

def main():
    titles = listAsCsv()
    titleList = titles.getTitlesList()

    for title in titleList:
        

if __name__ == "__main__":
    main()
