import sys
from typing import Iterable
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from helper.translateToUrlPath import translateToUrlPath

"""
routing pattern,

domain:     https://reelgood.com
tv shows:   /show
movie:      /movie
"""


class webScrapeEachTitleDetail():
    """
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


    def scrapeHtmlPageSelenium(self):
        """ Extract the HTML page by Selenium, then convert the Selenium object to BeautifulSoup object, and save it in class object.
        
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

        # writeToFile(html_text, "extracted_html_text", "html")
        # writeToFile(self.html_page_soup_object, "extracted_html_parsed", "html")
        # print(type(self.html_page_soup_object))


    def scrapeHtmlPageBeatifulSoup(self):
        """ Get the HTML page by BeatifulSoup, then save it in class object.
        
        Return: `None`
        """
        
        html_text = requests.get(self.url).text
        self.html_page_soup_object = BeautifulSoup(html_text, 'html.parser')

        # writeToFile(html_text, "extracted_html_text", "html")
        # writeToFile(self.html_page_soup_object, "extracted_html_parsed", "html")
        # print(type(self.html_page_soup_object))


    def getHtmlPage(self) -> BeautifulSoup.new_tag:
        """
        Return
        ------
        `BeautifulSoup object`, the parsed HTML page 
        """
        return self.html_page_soup_object


    def getDescription(self) -> str:
        p = self.html_page_soup_object.find('p', itemprop="description")
        for x in p:
            return str(x)
        return


    def getLink(self) -> list:
        ls = []
        for link in self.html_page_soup_object.find_all('a', itemprop="url"):
            ls.append(str(link.get('href'))+"\n")
            # print(link.get('href'))
        return ls



def writeToFile(content: Iterable[str], 
                file_name: str = "extracted",
                file_type: str = "txt",
                file_path: str = "test"):

    print(f'> writing "{file_name}.{file_type}" to path "/{file_path}/"', end = '')

    if isinstance(content, list):
        if not isinstance(content[0], str):
            content = [str(c) for c in content]
    elif not isinstance(content, str):
        content = str(content)

    # Program to show various ways to read and
    # write data in a file.
    file1 = open(f"{file_path}/{file_name}.{file_type}", "w")
    
    file1.writelines(content)
    file1.close() #to change file access modes

    print('\t ==> DONE!')


if __name__ == "__main__":

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
    title = 'Lady Bird'
    year = '2017'

    scraper = webScrapeEachTitleDetail()
    scraper.setUrl(url_domain, movie_or_show, title, year)
    
    scraper.scrapeHtmlPageBeatifulSoup()
    soup = scraper.getHtmlPage()    #scraper.html_page_soup_object
    writeToFile(soup, "extracted_html_soup", "html")
    
    scraper.scrapeHtmlPageSelenium()
    soup = scraper.html_page_soup_object    #scraper.getHtmlPage()
    writeToFile(soup, "extracted_html_selenium", "html")

    description = scraper.getDescription()
    print(description[:20])
    # print(type(description))
    writeToFile(description, "extracted_description")

    links = scraper.getLink()
    print(links)
    writeToFile(links, "extracted_links")
