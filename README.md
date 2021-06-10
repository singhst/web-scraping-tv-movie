# web-scraping-tv-movie

A program to scrap TV Shows and Movies from [web page](https://reelgood.com/). Stores the scraped data in .csv format.

Data format in the web page: HTML table 


## Usage

1. `main-scrap-web-data.py`

    Use the following command to scrap data from web.  

    `-m`: option; to scrape the `Movies` table

    `-t`: option; to scrape the `TV Shows` table

    `trend`: argument (optional); to scrape trending `Movies` or `TV shows`

    ```sh
    $ python main-scrap-web-data.py -m OR -t <AND trend (optional)>
    ```

    ### Example 1

    Shows reminder message if no argument presents.

    <img src="img\terminal-run-prog-no-args.png" style="zoom:50%;"/>

    ### Example 2

    Extract `trending TV Shows` at 2021.05.28.

    Terminal, run the program:

    ```sh
    $ python main-scrap-web-data.py -t trend
    ```

    <img src="img\terminal-run-prog-args-tv-trend.png" style="zoom:50%;"/>

    Sample of the scraped data, the first three TV titles match with the table shown in web page:

    <img src="img\csv-tv-trend.png" style="zoom:40%;"/>

    Web page:

    <img src="img\reelgood-data-trend-tv-20210528.png" style="zoom:50%;"/>


## Missing features

1. Save scrape table data into mysql `main-scrape-title-list.py`
2. Log the can't-find title of movie/TV show
2. not finish `def extractCastCrew(self) -> list:` in `webScrapeEachTitleDetail.py`


## **NEED CHANGE ** Note - Program Structure

`main-scrap-web-data.py`: Main program to extract table data from web page.

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
    
    URL Slug:   /{title of movie or TV show}

    E.g.

    1.  movie name: Godzilla vs. Kong
        URL:        https://reelgood.com/movie/godzilla-vs-kong-2020

    2.  TV show name:   Loki
        URL:            https://reelgood.com/show/loki-2021
    ```


## Note - When continuously scraping

Must need to open and close the browser to perform continuous scraping.

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