from typing import Iterable
import requests
from bs4 import BeautifulSoup

"""
routing pattern,

domain:     https://reelgood.com
tv shows:   /show
movie:      /movie
"""


def writeToFile(content: Iterable[str], 
             file_name: str = "extracted",
             file_type: str = "txt"):

    if isinstance(content, list):
        if not isinstance(content[0], str):
            content = [str(c) for c in content]
    elif not isinstance(content, str):
        content = str(content)

    # Program to show various ways to read and
    # write data in a file.
    file1 = open(f"test/{file_name}.{file_type}","w")
    
    file1.writelines(content)
    file1.close() #to change file access modes


def getDescription() -> str:
    p = soup.find('p', itemprop="description")
    for x in p:
        return str(x)
    return


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
    vgm_url = 'https://reelgood.com/movie/the-intouchables-2011'

    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    writeToFile(soup, "extracted_html", "html")
    
    content = getDescription()
    print(content)
    print(type(content))
    writeToFile(content, "extracted_description")

    links = getLink()
    print(links)
    writeToFile(links, "extracted_links")