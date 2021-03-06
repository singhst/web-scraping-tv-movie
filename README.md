# web-scraping-tv-movie

A program to scrap TV Shows and Movies from [web page](https://reelgood.com/). Stores the scraped data in MySQL server and a backup in .csv format.

Data format in the web page: HTML table, JSON


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

        <img src="img\csv-allmovies.png" style="zoom:30%;"/>

        Web page:

        <img src="img\reelgood-data-allmovies.png" style="zoom:30%;"/>


2. `main-scrape-each-title-detail.py`

    To scrape the details of each movie/TV show continuously. This programe keeps opening and closing the Chrome browser.

    https://user-images.githubusercontent.com/71545537/123521711-f1a8e080-d6ea-11eb-9894-180d49966f3d.mp4

    The scraped JSON file,

    Overview:

    <img src="img\scraped-detail-json-person.png" style="zoom:40%;"/>
        
    Detail:
        
    <img src="img\scraped-detail-json-movie.png" style="zoom:50%;"/>
    
    mysql table after saving (1) overview, (2) ID in Reelgood.com:
    
    <img src="img\scraped-title-detail-mysql-table.png" style="zoom:70%;"/>

    A structured data in JSON format can be found in the webpage. Of course, it is shown after the JavaScript loaded.
    <img src="img\reelgood-inspect-html.png" style="zoom:30%;"/>

## Missing features

1. Log the can't-find titles of movies/TV shows
2. not finish `def extractCastCrew(self) -> list:` in `webScrapeEachTitleDetail.py`


## **NEED CHANGE ** Note - Program Structure

`main-scrap-title-list.py`: Main program to extract movie/TV show title list (table data) from web page.

`main-scrape-each-title-detail.py`: (Developing) Extract different media service providers (e.g. Netflix, Disney+) (example link: https://reelgood.com/show/friends-1994).


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


## Note - Reference Database ER Diagram

Follows `1NF` (First Normal Form) normalization rules:
- Each table cell should contain a single value.
- Each record needs to be unique.

Because one or more than one streaming platforms provide the same movie/TV show, the scrapped links for a movie/TV show can be more than one (e.g. `Netflix`, `Disney+`, `HBO` and `Amazon Prime` etc.). Follows `1NF` rule, storing links into one `movie` table cannot fulfill `1NF` rules. 

So, partition `movie` table into 2 tables:
1. `availability` table to store streaming links
2. `movie` table

`<img src="img\db-movies-erd.png" style="zoom:50%;"/>`

Credit to: [link](https://www.databasestar.com/sample-database-movies/)

https://examples.javacodegeeks.com/crud-operations-in-python-on-mysql/


## Browser driver Setup

Download `chromedriver.exe` (Windows) in this project directory 

OR 

Download `chromedriver` (Linux) under `/usr/local/bin`

[Downliad link](https://chromedriver.chromium.org/downloads)


## Python Runtime Setup

Set up python environment when it is a new env,

1. Check whether `virtualenv` is installed:

    ```shell
    $ python3 -m pip show virtualenv
    
    Name: virtualenv
    Version: 20.9.0
    Summary: Virtual Python Environment builder
    Home-page: https://virtualenv.pypa.io/
    Author: Bernat Gabor
    Author-email: gaborjbernat@gmail.com
    License: MIT
    Location: /Users/Sing/Library/Python/3.8/lib/python/site-packages
    Requires: six, backports.entry-points-selectable, platformdirs, distlib, filelock
    Required-by: 
    ```

    Install if don't have:

    ```shell
    $ python3 -m pip install virtualenv
    ```


2. Create new VirtualEnv:

    cd to your preferred file path:
    ```shell
    $ cd ...
    ```

    ```shell
    $ python3 -m venv venv
    ```

    Use `ls` to check:
    ```shell
    $ ls

    ... venv ...
    ```


3. Activate the VirtualEnv 

    Linux:

    ```shell
    $ source venv/bin/activate
    ```	
    OR	
    ```shell
    $ . venv/bin/activate
    ```
	
    Windows
    ```shell
    $ venv\Scripts\activate.bat
    ```


4. pip install requirements.txt:

    ```shell
    (venv) $ pip install -r requirements.txt
    ```


5. Export venv pip requirements.txt:

    ```shell
    (venv) $ pip freeze > requirements.txt
    ```
