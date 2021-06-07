import sys
from typing import Iterable
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import json

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from helper.translateToUrlPath import translateToUrlPath
from helper.folderHandler import folderCreate
from helper.writeToFile import writeToFile


"""
routing pattern,

domain:     https://reelgood.com
tv shows:   /show
movie:      /movie
"""


class webScrapeEachTitleDetail():
    """
    0. Initialize class,

        `> scraper = webScrapeEachTitleDetail()`

    1. Set URL, 

        `> scraper = webScrapeEachTitleDetail()`

        `> scraper.setUrl(url_domain, movie_or_show, title, year)`

    2. Scrape the web page,

        `> scraper.scrapeHtmlPageSelenium()`

    3. Extract movie/tv show data,

        `> scraper.extractTitleDetail()`
    
    4. Get movie/tv show (1) title (2) description (3) links (4) cast & crews

        `> title = scraper.title`

        `> description = scraper.description`

        `> links = scraper.title_links`

        `> cast_crew = scraper.cast_crew`

    """

    def __init__(self):
        
        # url pattern: `https://reelgood.com/{movie or show}/{title of movie or tv show (space is replaced by hyphen '-')}-{year}`
        # e.g.  https://reelgood.com/movie/lady-bird-2017
        self.url_domain = ''      # https://reelgood.com
        self.url_path_var1 = ''   # /movie OR /show
        self.url_path_var2 = ''   # /{title of movie or TV show}-{year}, space is replaced by hyphen `-`
        self.url_path_var3 = ''   # /{title of movie or TV show}-{year}
        
        self.url = ''
        self.html_page_soup_object = BeautifulSoup.new_tag
        self.meta_data = {}

        self.title_detail_dict = {}
        self.rg_id = ''
        self.title = ''
        self.description = ''
        self.title_links = Iterable[str]
        self.cast_crew = Iterable[str]


    def setUrl(self,
               url_domain: str,
               movie_or_show: str,
               title: str,
               year: str):
        """
        url_domain: `str`, e.g. `https://xxxx.com`
        
        movie_or_show: `str`, only accept `movie` or `show` because of the Reelgood url pattern.

        title: `str`, title of the movie/TV show

        year: `str`, publishing year
        """

        self.url_domain = url_domain        # https://reelgood.com
        self.url_path_var1 = movie_or_show  # /movie OR /show
        self.url_path_var2 = title          # /{title of movie or TV show}-{year}, space is replaced by hyphen `-`
        self.url_path_var3 = year           # /{title of movie or TV show}-{year}
        
        self.url = translateToUrlPath(url_domain, movie_or_show, title, year)
        print("> webScrapeEachTitleDetail, self.url =", self.url)


    def setUrlDirectly(self,
                       url: str):
        """ url: `str`
        
        e.g. 
        
        `_a_url = 'https://reelgood.com/movie/lady-bird-2017'`
        
        OR

        `_a_url = 'https://reelgood.com/show/the-good-doctor-2017'`
        
        `setUrlDirectly(url = _a_url)`
        """
        self.url = url


    def scrapeHtmlPageBeatifulSoup(self):
        """ Get the HTML page by BeatifulSoup, then save it in class object.
        
        Return: `None`
        """
        
        html_text = requests.get(self.url).text
        self.html_page_soup_object = BeautifulSoup(html_text, 'html.parser')

        # writeToFile(html_text, "extracted_html_text", "html")
        # writeToFile(self.html_page_soup_object, "extracted_html_parsed", "html")
        # print(type(self.html_page_soup_object))


    def scrapeHtmlPageSelenium(self):
        """
        (1) Extract the HTML page by Selenium, then convert the Selenium object to BeautifulSoup object, and save it in class object.
        
        (2) Save the extracted meta data in class object (`dict` type).

        Return: `None`
        """

        # Selenium settings
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        # options.binary_location = "/usr/bin/chromium"
        driver = webdriver.Chrome(chrome_options=options)
        
        # Selenium extracts html page from url
        driver.get(self.url)
        html_text = driver.page_source

        # Convert Selenium object into BeautifulSoup object
        self.html_page_soup_object = BeautifulSoup(html_text, 'html.parser')

        # structured json data is in the HTML tag <script type="text/javascript">
        self.meta_data = self.extractJsTagJson()


    def extractJsTagJson(self) -> dict:
        # structured json data is in the HTML tag <script type="text/javascript">
        bs_elems = self.html_page_soup_object.find_all('script', type='text/javascript')
        bs_single_elem = self.cleanMetaData(bs_elems)
        
        bs_single_elem = self.strToDict(bs_single_elem)

        return bs_single_elem['bootstrap']['entities']['entries']


    def cleanMetaData(self, bs_elems) -> str:
        temp_str = ''
        
        for x, i in zip(bs_elems, range(len(bs_elems))):
            if i == 7:
                # print(i)
                temp_str = x.string
                # print("> len(temp_str) =", len(temp_str))
                # print("> type(temp_str) =", type(temp_str))

        temp_str = temp_str.replace("_rg.update(", "")
        temp_str = temp_str.replace("})", "}")
        temp_str = temp_str.replace("\\u002F", "/")
        temp_str = temp_str.replace('undefined', '"undefined"')
        # print("> type(temp_str)=", type(temp_str))

        return temp_str


    def strToDict(self, string: str) -> dict:
        theJson = json.loads(string)
        # the result is a Python dictionary:
        print(type(theJson))
        return theJson


    def extractTitleDetail(self):
        """
        
        """
        _a_dict = self.meta_data.values()
        _a_dict = iter(_a_dict)
        self.title_detail_dict = next(_a_dict)

        # print("\t> self.title_detail_dict =", self.title_detail_dict)
        self.rg_id = self.title_detail_dict['rg_id']
        self.description = self.title_detail_dict['overview']
        self.title_links = self.title_detail_dict['availability']
        self.cast_crew = self.extractCastCrew()


    def extractCastCrew(self) -> dict:
        """NOT FINISHED.
        """
        search_key = 'person'
        # Using items() + list comprehension
        # Substring Key match in dictionary
        res = [val for key, val in self.meta_data.items() if search_key in key]
        return res


    def getHtmlPage(self) -> BeautifulSoup.new_tag:
        """
        Return
        ------
        `BeautifulSoup object`, the parsed HTML page 
        """
        return self.html_page_soup_object


    def getMetaData(self) -> dict:
        """
        Return
        ------
        `dict`, the metda data including (1) link (2) description (3) cast & crew
        """
        return self.meta_data


    def getDescription(self) -> str:
        p = self.html_page_soup_object.find('p', itemprop="description")
        for x in p:
            return str(x)
        return


    def getDescriptionFromMetaData(self) -> str:
        """
        Return
        ------
        `str`, Description
        """
        return self.description


    def getLink(self) -> list:
        ls = []
        for link in self.html_page_soup_object.find_all('a', itemprop="url"):
            ls.append(str(link.get('href'))+"\n")
            # print(link.get('href'))
        return ls


    def getLinkFromMetaData(self) -> list:
        return


# def writeToFile(content: Iterable[str], 
#                 file_name: str = "extracted",
#                 file_type: str = "txt",
#                 file_path: str = "test"):

#     print(f'> writing "{file_name}.{file_type}" to path "/{file_path}/"', end = '')

#     if isinstance(content, list):
#         if not isinstance(content[0], str):
#             content = [str(c) for c in content]
#     elif not isinstance(content, str):
#         content = str(content)

#     # Program to show various ways to read and
#     # write data in a file.
#     file1 = open(f"{file_path}/{file_name}.{file_type}", "w")
    
#     file1.writelines(content)
#     file1.close() #to change file access modes

#     print('\t ==> DONE!')


def main():

    current_path = os.getcwd()
    folder_name = 'temp_save'
    path = os.path.join(current_path, 'test')

    # Get TV show or Movie data
    export_path = folderCreate(path, folder_name)

    # vgm_url = 'https://www.vgmusic.com/music/console/nintendo/nes/'
    # vgm_url = 'https://reelgood.com/show/the-good-doctor-2017'
    # vgm_url = 'https://reelgood.com/show/startup-2016'
    # vgm_url = 'https://reelgood.com/movie/rogue-one-a-star-wars-story-2016'
    # vgm_url = 'https://reelgood.com/movie/hellboy-2019'
    # vgm_url = 'https://reelgood.com/movie/the-intouchables-2011'
    # vgm_url = 'https://reelgood.com/movie/3-idiots-2009'
    vgm_url = 'https://reelgood.com/movie/lady-bird-2017'
    
    url_domain = 'https://reelgood.com'
    movie_or_show = 'movie'
    title = 'Lady Bird' #'3 Idiots'
    year = '2017'       #2009

    scraper = webScrapeEachTitleDetail()
    scraper.setUrl(url_domain, movie_or_show, title, year)
    

    # scraper.scrapeHtmlPageBeatifulSoup()
    # soup = scraper.getHtmlPage()    #scraper.html_page_soup_object
    # writeToFile(soup, "extracted_html_soup", "html")
    

    scraper.scrapeHtmlPageSelenium()
    soup = scraper.html_page_soup_object    #scraper.getHtmlPage()
    writeToFile(soup,
                f"extracted_{title}_{year}_0_html_selenium", 
                "html", 
                export_path)

    meta_data = scraper.getMetaData()
    str_meta_data = json.dumps(meta_data)
    writeToFile(str_meta_data,
                f"extracted_{title}_{year}_1_meta", 
                "json", 
                export_path)

    scraper.extractTitleDetail()
    title_detail_dict = scraper.title_detail_dict
    writeToFile(json.dumps(title_detail_dict),
                f"extracted_{title}_{year}_2_{movie_or_show}_detail", 
                "json", 
                export_path)

    movie_id = scraper.rg_id
    movie_title = scraper.title
    description = scraper.description
    links = scraper.title_links
    cast_crew = scraper.cast_crew

    writeToFile(description,
                f"extracted_{title}_{year}_3_description",
                file_path=export_path)
    writeToFile(json.dumps(links),
                f"extracted_{title}_{year}_4_links",
                "json",
                export_path)
    writeToFile(json.dumps(cast_crew),
                f"extracted_{title}_{year}_4_links",
                "json",
                export_path)


    print("1) movie_id:", movie_id)
    print("2) movie_title:", movie_title)
    print("3) description[:20]:", description[:20])
    print(f"4) links[0]: {type(links)}, {links[0]}")
    print("5) cast_crew[0]:", cast_crew[0])


if __name__ == "__main__":
    main()
