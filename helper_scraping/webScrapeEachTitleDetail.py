from typing import Iterable
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import re

# The below use to change path
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
## Import the lib under new path
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
    1. Initialize class,

        `> scraper = webScrapeEachTitleDetail()`

    2. Set URL, 

        `> scraper.setUrl(url_domain, movie_or_show, title, year)`

    3. Scrape the web page,

        `> scraper.scrapeHtmlPageSelenium()`

    4. Extract movie/tv show data,

        `> scraper.extractTitleDetail()`
    
    5. Get movie/tv show (1) title (2) description (3) links (4) cast & crews

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
        self._title_links_dict_list = Iterable[dict]
        self.title_links = Iterable[str]
        self._cast_crew_dict_list = Iterable[dict]
        self.cast_crew = Iterable[str]


    def setUrl(self,
               movie_or_show: str,
               title: str,
               year: str,
               url_domain: str = 'https://reelgood.com'):
        """
        url_domain: `str`, e.g. `https://xxxx.com`
        
        movie_or_show: `str`, only accept `movie` or `show` because of the Reelgood url pattern.

        title: `str`, title of the movie/TV show, e.g. `Godzilla vs. Kong`

        year: `str`, publishing year
        """

        self.url_domain = url_domain        # https://reelgood.com
        self.url_path_var1 = movie_or_show  # /movie OR /show
        self.url_path_var2 = title          # /{title of movie or TV show}-{year}, space is replaced by hyphen `-`
        self.url_path_var3 = year           # /{title of movie or TV show}-{year}
        
        self.url = translateToUrlPath(url_domain, movie_or_show, title, year)
        print("> webScrapeEachTitleDetail, self.url =", self.url)

        self.title = title


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


    def scrapeHtmlPageSelenium(self) -> bool:
        """
        (1) Extract the HTML page by Selenium, then convert the Selenium object to BeautifulSoup object, and save it in class object.
        
        (2) Save the extracted meta data in class object (`dict` type).

        Return
        ------
        `bool` 
        
        1. `True`:  Detail info of this movie/TV show exits in the web page
        2. `False`: Web page does not exist
        """

        # Selenium settings
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        # options.binary_location = "/usr/bin/chromium"
        self.driver = webdriver.Chrome(chrome_options=options) # Create browser 

        # Selenium extracts html page from url
        # self.driver.delete_all_cookies(); # Deletes all the cookies
        self.driver.get(self.url)
        html_text = self.driver.page_source

        self.driver.quit()  # Close browser 

        # Convert Selenium object into BeautifulSoup object
        self.html_page_soup_object = BeautifulSoup(html_text, 'html.parser')

        # structured json data is in the HTML tag <script type="text/javascript">
        if self.extractJsTagJson() is not None:
            self.meta_data = self.extractJsTagJson()
            return True
        
        return False



    def extractJsTagJson(self) -> dict:
        """Because we found that the structural info of a movie/tv show is stored inside a JSON 
        under HTML tag <script type="text/javascript">
        """
        try:
            # structured json data is in the HTML tag <script type="text/javascript">
            bs_elems = self.html_page_soup_object.find_all('script', type='text/javascript')
            bs_single_elem = self.cleanMetaData(bs_elems)
            
            bs_single_elem = self.strToDict(bs_single_elem)

            return bs_single_elem['bootstrap']['entities']['entries']

        except:
            # print(f"> `{self.title}` not found!")
            return None


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
        # temp_str = temp_str.replace("\\u002F", "/")
        # temp_str = self.unicodeToChar(temp_str)
        temp_str = temp_str.replace('undefined', '"undefined"')
        # print("> type(temp_str)=", type(temp_str))

        return temp_str


    def unicodeToChar(self, input_str: str) -> str:
        # find()
        return input_str


    def strToDict(self, string: str) -> dict:
        theJson = json.loads(string)
        # the result is a Python dictionary:
        print(type(theJson))
        return theJson


    def extractTitleDetail(self):
        """
        self.title_detail_dict = {}
        self.rg_id = ''
        self.title = ''
        self.description = ''
        self.title_links = Iterable[str]
        self.cast_crew = Iterable[str]
        """
        #First item in dict is the info about the movie/tv show 
        _a_dict = self.meta_data.values()
        _a_dict = iter(_a_dict)
        self.title_detail_dict = next(_a_dict)

        # print("\t> self.title_detail_dict =", self.title_detail_dict)
        self.rg_id = self.title_detail_dict['rg_id']
        self.title = self.title_detail_dict['title']
        self.description = self.title_detail_dict['overview']
        self.title_links, self._title_links_dict_list = self.extractLinks()
        self.cast_crew, self._cast_crew_dict_list = self.extractCastCrew()


    def extractLinks(self) -> list:
        """
        Return 
        ------
        links: `dict`, {"links": ["www.xxx", "www.yyy", "www.zzz"]}

        links_dict_list: `Iterable[dict]`
        """
        links_dict_list = self.title_detail_dict['availability'] #it is a list of dict
        links = {"links": [link_dict['source_data']['web_link'] for link_dict in links_dict_list]}
        return links, links_dict_list


    def extractCastCrew(self) -> list:
        """NOT FINISHED.
        Missing the roles of each cast & crew. need to match by persion ID.

        Return 
        ------
        cast_crew: `dict`
        
        cast_crew_dict_list: `Iterable[dict]`
        """
        search_key = 'person'
        # Using items() + list comprehension
        # Substring Key match in dictionary
        cast_crew_dict_list = [val for key, val in self.meta_data.items() if search_key in key]
        cast_crew = cast_crew_dict_list

        return cast_crew, cast_crew_dict_list


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
        """No use"""
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
        """No use"""
        ls = []
        for link in self.html_page_soup_object.find_all('a', itemprop="url"):
            ls.append(str(link.get('href'))+"\n")
            # print(link.get('href'))
        return ls


def main():
    # Create folders to save scraped data
    current_path = os.getcwd()
    path = os.path.join(current_path, 'test')

    temp_save_path = folderCreate(path, 'temp_save')
    demo_save_path = folderCreate(path, 'demo_save')

    # vgm_url = 'https://www.vgmusic.com/music/console/nintendo/nes/'
    # vgm_url = 'https://reelgood.com/show/the-good-doctor-2017'
    # vgm_url = 'https://reelgood.com/show/startup-2016'
    # vgm_url = 'https://reelgood.com/movie/rogue-one-a-star-wars-story-2016'
    # vgm_url = 'https://reelgood.com/movie/hellboy-2019'
    # vgm_url = 'https://reelgood.com/movie/the-intouchables-2011'
    # vgm_url = 'https://reelgood.com/movie/3-idiots-2009'
    # vgm_url = 'https://reelgood.com/movie/lady-bird-2017'
    
    """
    ('Godzilla vs. Kong', '2020')
    ('Joker', '2019') 
    ('Lady Bird', '2017') 
    ('3 Idiots', '2009') 
    ('spirited away', '2003')
    ('The Intouchables', '2011')
    """
    url_domain = 'https://reelgood.com'
    movie_or_show = 'movie'
    title, year = ('3 Idiots', '2009')

    # Remove title's symbols ==> keep only letter, number and space char
    title_no_symbol = re.sub(r'[^a-zA-Z0-9 ]+', '', title)
    title_no_symbol = title_no_symbol.replace(' ', '_')

    # Get TV show or Movie data
    scraper = webScrapeEachTitleDetail()
    scraper.setUrl(url_domain=url_domain, movie_or_show=movie_or_show, title=title, year=year)
    

    # Get HTML code
    # and Check whether the info of this movie/tv show exist or not
    if not scraper.scrapeHtmlPageSelenium():
        print(f"> `{title}, {year}` not found!")
    else:
        soup = scraper.html_page_soup_object    #scraper.getHtmlPage()
        writeToFile(soup,
                    f"extracted_{title_no_symbol}_{year}_0_html_selenium", 
                    "html", 
                    temp_save_path)


        # Get .js json from <script type='text/javascript'> tag 
        # This json contains all information about the movie/tv show
        meta_data = scraper.getMetaData()
        str_meta_data = json.dumps(meta_data)
        writeToFile(str_meta_data,
                    f"extracted_{title_no_symbol}_{year}_1_meta", 
                    "json", 
                    temp_save_path)


        # Extract (1) description (2) links (3) cast & crew etc.
        scraper.extractTitleDetail()
        title_detail_dict = scraper.title_detail_dict
        writeToFile(json.dumps(title_detail_dict),
                    f"extracted_{title_no_symbol}_{year}_2_{movie_or_show}_detail", 
                    "json", 
                    temp_save_path)


        movie_id = scraper.rg_id
        movie_title = scraper.title
        description = scraper.description
        links = scraper.title_links
        cast_crew = scraper.cast_crew

        _title_links_dict_list = scraper._title_links_dict_list
        _cast_crew_dict_list = scraper._cast_crew_dict_list

        writeToFile(description,
                    f"extracted_{title_no_symbol}_{year}_description",
                    file_path=demo_save_path)
        writeToFile(json.dumps(links),
                    f"extracted_{title_no_symbol}_{year}_links",
                    "json",
                    demo_save_path)
        writeToFile(json.dumps(cast_crew),
                    f"extracted_{title_no_symbol}_{year}_cast_crew",
                    "json",
                    demo_save_path)


        writeToFile(json.dumps(_title_links_dict_list),
                    f"extracted_{title_no_symbol}_{year}_4_links_dict_list",
                    "json",
                    temp_save_path)
        writeToFile(json.dumps(_cast_crew_dict_list),
                    f"extracted_{title_no_symbol}_{year}_5_cast_crew_dict_list",
                    "json",
                    temp_save_path)


        print("1) movie_id:", movie_id)
        print("2) movie_title:", movie_title)
        print("3) description:", description)
        print(f"4) links: {type(links)}, {links}")
        print("5) cast_crew[0]:", cast_crew[0])


if __name__ == "__main__":
    main()
