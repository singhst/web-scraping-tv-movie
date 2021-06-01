from typing import Iterable
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

"""
routing pattern,

domain:     https://reelgood.com
tv shows:   /show
movie:      /movie
"""


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


def getHtmlPage(url) -> BeautifulSoup.new_tag:
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    # print(type(self.soup))
    
    return soup


def getDescription(soup) -> str:
    p = soup.find('p', itemprop="description")
    for x in p:
        return str(x)
    return


def clickBtnGetLink() -> Iterable[str]:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    # options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(chrome_options=options)
    url = 'https://reelgood.com/uk/movie/3-idiots-2009'
    driver.get(url)

    # ActionChains(driver).move_by_offset(0, 300).click().perform()
    driver.find_element_by_xpath("//button[@class='css-hpmncj eyx6tna3']").click().perform()


def getLink():
    ls = []
    for link in soup.find_all('a', itemprop="url"):
        ls.append(str(link.get('href'))+"\n")
        # print(link.get('href'))
    return ls


if __name__ == "__main__":
    # vgm_url = 'https://www.vgmusic.com/music/console/nintendo/nes/'
    # vgm_url = 'https://reelgood.com/show/the-good-doctor-2017'
    # vgm_url = 'https://reelgood.com/show/startup-2016'
    # vgm_url = 'https://reelgood.com/movie/rogue-one-a-star-wars-story-2016'
    # vgm_url = 'https://reelgood.com/movie/hellboy-2019'
    # vgm_url = 'https://reelgood.com/movie/the-intouchables-2011'
    # vgm_url = 'https://reelgood.com/uk/movie/3-idiots-2009'
    vgm_url = 'https://reelgood.com/movie/lady-bird-2017'

    # html_text = requests.get(vgm_url).text
    # soup = BeautifulSoup(html_text, 'html.parser')
    soup = getHtmlPage(vgm_url)
    writeToFile(soup, "extracted_html_parsed", "html")
    
    content = getDescription(soup)
    # print(content)
    print(type(content))
    writeToFile(content, "extracted_description")

    links = getLink()
    print(links)
    writeToFile(links, "extracted_links")