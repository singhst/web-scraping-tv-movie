"""
https://stackoverflow.com/questions/44635753/how-to-scrape-website-data-after-clicking-more-button
"""

import time
from typing import Iterable

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
# options.binary_location = "/usr/bin/chromium"
driver = webdriver.Chrome(chrome_options=options)

# driver.get('https://reelgood.com/uk/movie/3-idiots-2009')
driver.get('https://reelgood.com/movie/lady-bird-2017')


# click "Stream Movie" button
moreButton = driver.find_element_by_xpath("//button[@class='css-hpmncj eyx6tna3']")
moreButton.click()


# wait = WebDriverWait(driver, 10)
# element = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "css-rshlkp e126mwsw1")))

time.sleep(4)

# in pop-up window, click "Rent/Buy from xxx"
moreButton = driver.find_element_by_xpath("//button[@class='css-rshlkp e126mwsw1']")
moreButton.click()
moreButton.click()


html_source = driver.page_source
writeToFile(html_source, "extracted_after_btn_click", 'html')