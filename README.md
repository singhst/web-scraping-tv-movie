# web-scraping-tv-movie

A program to scrap TV Shows and Movies from [web page](https://reelgood.com/). Stores the scraped data in .csv format.

Data format in the web page: HTML table 


## Usage

1. `main-scrap-title-list.py`

    Use the following command to scrap data from web. The scraped movie/TV show title list stores in MySQL server while keeping a copy in .csv format.

    `-m`: option; to scrape the `Movies` table

    `-t`: option; to scrape the `TV Shows` table

    `trend`: argument (optional); to scrape trending `Movies` or `TV shows`

    ```sh
    $ python main-scrap-title-list.py -m OR -t <AND trend (optional)>
    ```

    ### Example 1

    Shows reminder message if no argument presents.

    <img src="img\terminal-run-prog-no-args.png" style="zoom:50%;"/>

    ### Example 2

    Extract `trending TV Shows` at 2021.05.28.

    Terminal, run the program:

    ```sh
    $ python main-scrap-title-list.py -t trend
    ```

    <img src="img\terminal-run-prog-args-tv-trend.png" style="zoom:50%;"/>

    ### The Scraped Title List
    
    1. Title list stored in MySQL server.

        Total row count:
        
        <img src="img\scraped-title-list-mysql-row-count.png" style="zoom:50%;"/>

        Table in Database in MySQL server:
        
        <img src="img\scraped-title-list-mysql-table.png" style="zoom:50%;"/>

    2. A copy of title list in .csv format.

        Sample of the scraped data, the first three TV titles match with the table shown in web page:

        <img src="img\csv-allmovies.png" style="zoom:40%;"/>

        Web page:

        <img src="img\reelgood-data-allmovies.png" style="zoom:30%;"/>


2. `main-scrape-each-title-detail.py`

    To scrape the details of each movie/TV show continuously. This programe keeps opening and closing the Chrome browser.

    xxxx

    The scraped JSON file,

    Overview:

    <img src="img\scraped-detail-json-person.png" style="zoom:50%;"/>
        
    Detail:
        
    <img src="img\scraped-detail-json-movie.png" style="zoom:50%;"/>
    
    mysql table after saving (1) overview, (2) ID in Reelgood.com:
    
    <img src="img\scraped-title-detail-mysql-table.png" style="zoom:70%;"/>

    A structured data in JSON format can be found in the webpage:
    <img src="img\reelgood-inspect-html.png" style="zoom:30%;"/>

## Missing features

1. Log the can't-find titles of movies/TV shows
2. not finish `def extractCastCrew(self) -> list:` in `webScrapeEachTitleDetail.py`


## **NEED CHANGE ** Note - Program Structure

`main-scrap-title-list.py`: Main program to extract table data from web page.

`main-scrap-link.py`: (Developing) Extract different media service providers (e.g. Netflix, Disney+) (example link: https://reelgood.com/show/friends-1994).

`combine-csv.py`: Combine the separated extractde .csv files into one. 


## Note - Routing in the web

1. Get movie/TV show title list.

    ```
    Domain:     https://reelgood.com
    
    URL path:   /tv AND /genre AND /crime

    Query parameters:   ?filter-imdb_end=6.9&filter-imdb_start=4
                        &filter-rg_end=70&filter-rg_start=30
                        &filter-year_end=2018&filter-year_start=1998
    ```

2. Get detail info of each movie/TV show

    ```
    Domain:     https://reelgood.com

    URL path:   /movie  OR  /show
    
    URL Slug:   /{title of movie or TV show}-{year}

    E.g.

    1.  movie name: Godzilla vs. Kong
        URL:        https://reelgood.com/movie/godzilla-vs-kong-2020

    2.  TV show name:   Loki
        URL:            https://reelgood.com/show/loki-2021
    ```


## Note - When continuously scraping

Must need to open and close the browser to perform continuous scraping.

Reason: 
Guess, browser cookie related issue.

See [webScrapeEachTitleDetail.py](https://github.com/singhst/web-scraping-tv-movie/blob/master/helper_scraping/webScrapeEachTitleDetail.py)

```python
def scrapeHtmlPageSelenium(self) -> bool:
    ...

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

    ...
```


## Note - Reference Database ERD

Credit to: [link](https://www.databasestar.com/sample-database-movies/)

<img src="img\db-movies-erd.png" style="zoom:50%;"/>


https://examples.javacodegeeks.com/crud-operations-in-python-on-mysql/


## Browser driver Setup

Download `chromedriver.exe` (Windows) in this project directory 

OR 

Download `chromedriver` (Linux) under `/usr/local/bin`

[Downliad link](https://chromedriver.chromium.org/downloads)


## Python Runtime Setup

Set up python environment when it is a new env,

1. Create new VirtualEnv:

    ```sh
    $ virtualenv venv
    ```

2. Activate the VirtualEnv 

    Linux:

    ```sh
    $ source venv/bin/activate
    ```	
    OR	
    ```sh
    $ . venv/bin/activate
    ```
	
    Windows
    ```sh
    $ venv\Scripts\activate.bat
    ```


3. pip install requirements.txt:

    ```sh
    $ pip install -r requirements.txt
    ```


4. Export venv pip requirements.txt:

    ```sh
    $ pip freeze > requirements.txt
    ```