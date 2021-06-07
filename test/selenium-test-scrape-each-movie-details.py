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

start_time = 0
end_time = 0

def writeToFile(content: Iterable[str],
                file_name: str = "extracted",
                file_type: str = "txt",
                file_path: str = "test"):

    print(
        f'> writing "{file_name}.{file_type}" to path "/{file_path}/"', end='')

    if isinstance(content, list):
        if not isinstance(content[0], str):
            content = [str(c) for c in content]
    elif not isinstance(content, str):
        content = str(content)

    # Program to show various ways to read and
    # write data in a file.
    file1 = open(f"{file_path}/{file_name}.{file_type}", "w")

    file1.writelines(content)
    file1.close()  # to change file access modes

    print('\t ==> DONE!')


def clicking_on_web(driver):
    # click "Stream Movie" button
    moreButton = driver.find_element_by_xpath("//button[@class='css-hpmncj eyx6tna3']")
    moreButton.click()

    # Wait for a while
    # wait = WebDriverWait(driver, 10)
    # element = wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[@class='css-1ks2bp0 e126mwsw1']")))
    time.sleep(2)

    # in pop-up window, click "Rent/Buy from xxx"
    moreButton = driver.find_element_by_xpath("//button[@class='css-rshlkp e126mwsw1']")
    moreButton.click()

    jsScript = driver.find_element_by_xpath("//script[@type='text/javascript']")
    # script_text = driver.find_element_by_xpath("//script[contains(.,'_rg.update(')]").text
    script_text = str(jsScript.get_attribute("outerHTML"))
    print(script_text) 

    # Wait for a while
    time.sleep(2)


def no_clicking_on_web(driver):
    # Scrap the web page containing (1) description text, (2) Stream links (3) Rent/But links
    html_source = driver.page_source
    print("> type(html_source) =", type(html_source))

    driver.close()

    bsObj = BeautifulSoup(html_source, 'html.parser')
    bsElems = bsObj.find_all('script', type='text/javascript')

    string = ''
    # ary = []
    for x, i in zip(bsElems, range(len(bsElems))):
        if i == 7:
            print(i)
            string = x.string
            print("> len(string) =", len(string))
            print("> type(string) =", type(string))

            # btyes_string = bytes(string, 'UTF-8')
            # print("> len(string) =", len(string))
            # print("> type(string) =", type(string))

            # ary.append(string)

    string = string.replace("_rg.update(", "")
    string = string.replace("})", "}")
    string = string.replace("\\u002F", "/")
    string = string.replace('undefined', '"undefined"')
    print("> type(string)=", type(string))

    import json
    theJson = json.loads(string)
    # the result is a Python dictionary:
    print(type(theJson))

    end_time = time.time()

    writeToFile(html_source, "extracted_html_source", 'html')
    # writeToFile(script_text, "extracted_script_text", "html")
    writeToFile(string, "extracted_data", 'json')
    print("time =", end_time - start_time)


if __name__ == "__main__":
    
    start_time = time.time()

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    # options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(chrome_options=options)
    # driver.get('https://reelgood.com/uk/movie/3-idiots-2009')
    driver.get('https://reelgood.com/movie/lady-bird-2017')

    # clicking_on_web(driver)
    no_clicking_on_web(driver)