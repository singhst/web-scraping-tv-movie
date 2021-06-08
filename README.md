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


## **NEED CHANGE ** Note - Program Structure

```sh
> tree /F
.
│   combine-and-clean-csv.py
│   main-scrape-each-title-detail.py
│   main-scrape-title-list.py
│
├───db_helper
│       databaseCsv.py
│       databaseMongoDB.js
│       databaseMongoDB.py
│       databaseMySQL.js
│       databaseMySQL.py
│       databaseSQLite.py
│       __init__.py
│   
├───helper
│       folderHandler.py
│       getCmlArg.py
│       tempStorage.py
│       test-import-module.py
│       translateToUrlPath.py
│       writeToFile.py
│       writeToFile.txt
│       __init__.py
│
├───reelgood-database
│   │   all-movies.csv
│   │   all-tv.csv
│   │
│   ├───(backup)
│   ├───movies
│   ├───trending-movies
│   ├───trending-tv
│   └───tv
│
└───webdriver
```

`main-scrap-web-data.py`: Main program to extract table data from web page.

`main-scrap-link.py`: (Developing) Extract different media service providers (e.g. Netflix, Disney+) (example link: https://reelgood.com/show/friends-1994).

`combine-csv.py`: Combine the separated extractde .csv files into one. 


## Note - Routing in the web

Get movie/TV show title list.

```
https://reelgood.com
/tv
/genre
/crime
?filter-imdb_end=6.9&filter-imdb_start=4
&filter-rg_end=70&filter-rg_start=30
&filter-year_end=2018&filter-year_start=1998
```


## Note - Reference Database ERD

Credit to: [link](https://www.databasestar.com/sample-database-movies/)

<img src="img\db-movies-erd.png" style="zoom:50%;"/>


## Setup

Set up python environment when it is a new env,

1. Create new VirtualEnv:

    ```sh
    > virtualenv venv
    ```

2. Activate the VirtualEnv 

    Linux:

    ```sh
    $> source venv/bin/activate
    ```	
    OR	
    ```sh
    $> . venv/bin/activate
    ```
	
    Windows
    ```sh
    $> venv\Scripts\activate.bat
    ```


3. pip install requirements.txt:

    ```sh
    > pip install -r requirements.txt
    ```


Export venv pip requirements.txt:

```sh
> pip freeze > requirements.txt
```