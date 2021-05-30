import requests
from bs4 import BeautifulSoup

"""
routing pattern,

domain:     https://reelgood.com
tv shows:   /show
movie:      /movie


"""

# vgm_url = 'https://www.vgmusic.com/music/console/nintendo/nes/'
# vgm_url = 'https://reelgood.com/show/the-good-doctor-2017'
# vgm_url = 'https://reelgood.com/show/startup-2016'
vgm_url = 'https://reelgood.com/movie/rogue-one-a-star-wars-story-2016'
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser')


def writeTxt(content: str):
    # Program to show various ways to read and
    # write data in a file.
    file1 = open("test/extracted_page.html","w")
    
    file1.writelines(content)
    file1.close() #to change file access modes

class webScraping():

    def __init__(self,
                 url_domain: str,
                 movie_or_tv_show: str,
                 title: str):
        self.url_domain = url_domain        # https://reelgood.com
        self.url_path_var1 = movie_or_tv_show   # /movie OR /show
        self.url_path_var2 = title              # /{title of movie or TV show}


    def getDescription(self) -> str:
        p = soup.find('p', itemprop="description")
        for x in p:
            return str(x)
        return


    def getLink(self):



if __name__ == "__main__":
    url_domain = 'https://reelgood.com'

    scrapper = webScraping()
    content = getDescription()
    print(content)
    print(type(content))
    # writeTxt(content)

