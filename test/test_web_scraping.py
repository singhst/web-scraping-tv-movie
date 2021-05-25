import urllib
from bs4 import BeautifulSoup
import selenium
import pandas as pd

def get_table_data(url: str, class_of_table: str) -> pd.DataFrame:
    
    # add User-Agent to header to pretend as browser visit, more detials can be found in FireBug plugin    
    # if we don't add the below, error message occurs. ERROR: urllib.error.HTTPError: HTTP Error 403: Forbidden
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', {'class': class_of_table})
    columns = [th.text.replace('\n', '') for th in table.find('tr').find_all('th')]
    # print(columns)

    trs = table.find_all('tr')[1:]
    rows = list()
    for tr in trs:
        rows.append([td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')])

    df = pd.DataFrame(data=rows, columns=columns)
    return df

def click_load_more_button():
    pass


url = 'https://reelgood.com/curated/trending-picks?offset=25000'
class_of_table = 'css-1179hly'
df = get_table_data(url, class_of_table)
print(df)
print(df.shape)