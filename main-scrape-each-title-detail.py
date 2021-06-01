"""
routing pattern,

domain:     https://reelgood.com
tv shows:   /show
movie:      /movie
"""

import requests
from bs4 import BeautifulSoup

from helper.translateToUrlPath import translateToUrlPath
from helper.getCmlArg import getCmlArg
from helper.tempStorage import tempStorage
from helper.writeToFile import writeToFile
from db_helper.databaseCsv import databaseCsv


class webScrapeEachTitleDetail():
    """
    url_domain: e.g. `https://xxxx.com`
    
    movie_or_show: `str`, only accept `movie` or `show` because of the Reelgood url pattern.

    title: `str`, title of the movie/TV show

    year: `str`, publishing year
    """

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
        print("> webScrapeEachTitleDetail, self.url =", self.url)

        self.soup = ''
        self.getHtmlPage()

    def getHtmlPage(self) -> BeautifulSoup.new_tag:
        html_text = requests.get(self.url).text
        self.soup = BeautifulSoup(html_text, 'html.parser')

        # writeToFile(html_text, "extracted_html_text", "html")
        # writeToFile(self.soup, "extracted_html_parsed", "html")
        # print(type(self.soup))
        
        return self.soup

    def getDescription(self) -> str:
        p = self.soup.find('p', itemprop="description")
        for x in p:
            return str(x)
        return

    def getLink(self):
        pass


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
    url_domain = 'https://reelgood.com'

    # Get argument from command line
    _url_path, movies_or_tv = getCmlArg()
    movie_or_show = movies_or_tv.replace('movies', 'movie').replace('tv', 'show')
    # print("url_path =", url_path)
    # print("movies_or_tv =", movies_or_tv)

    table = databaseCsv(movies_or_tv)
    titleList = table.getColumnByColName('Title')
    yearList = table.getColumnByColName('Year')
    # print(titleList[:10])

    storage = tempStorage()
    links = ['']

    # scrape (1) links, (2) description text, (3) 
    for title, year, i in zip(titleList, yearList, range(len(titleList))):
        print("> index: ", i)
        scraper = webScrapeEachTitleDetail(url_domain, movie_or_show, title, year)
        try:
            description = scraper.getDescription()
            print(f"\t> description: '{description[:30]}'")
            # links = scraper.getStreamRentBuyLinks() # under developing
        except:
            description = ''
        storage.addItem(movie_or_show, title, year, description, links)
    
    print(len(storage.getStoredItems()))

    filehandler = open('/reelgood-database/save.txt', 'wt')
    data = str(storage.getStoredItems())
    filehandler.write(data)


if __name__ == "__main__":
    main()
