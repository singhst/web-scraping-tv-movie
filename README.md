# web-scraping-tv-movie

A program to scrap TV Shows and Movies from [web page](https://reelgood.com/). Stores the scraped data in .csv format.

Data format in the web page: HTML table 


## Usage

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


## Note - Program Structure

```
.
|______ reelgood-database/
|       |______ tv/
|       |       |______ xxx.csv
|       |       |______ ...
|       |______ movie/
|       |______ tv-trend/
|       |______ movie-trend/
|______ main-scrap-web-data.py
|______ main-scrap-link.py
|______ combine-csv.py
```

`main-scrap-web-data.py`: Main program to extract table data from web page.

`main-scrap-link.py`: (Developing) Extract different media service providers (e.g. Netflix, Disney+) (example link: https://reelgood.com/show/friends-1994).

`combine-csv.py`: Combine the separated extractde .csv files into one. 


## Note - Routing in the web
```
https://reelgood.com
/tv
/genre
/crime
?filter-imdb_end=6.9&filter-imdb_start=4
&filter-rg_end=70&filter-rg_start=30
&filter-year_end=2018&filter-year_start=1998
```
