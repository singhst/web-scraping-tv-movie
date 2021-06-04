
def click_btn_by_xy_coord():
    from selenium import webdriver
    from selenium.webdriver.common.action_chains import ActionChains

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    # options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("http://www.google.com")
    ActionChains(driver).move_by_offset(0, 0).click().perform() #left mouse click, 200 is the x coordinate and 100 is the y coordinate
    ActionChains(driver).move_by_offset(0, 0).context_click().perform() #Right-click


def click_btn_by_class_name():
    from selenium import webdriver
    from selenium.webdriver.common.action_chains import ActionChains
    import time

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    # options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://www.tokopedia.com/sunxin')

    ActionChains(driver).move_by_offset(0, 300).click().perform()
    driver.find_element_by_xpath("//button[@class='css-62yvak-unf-btn e1ggruw00']").click().perform()


if __name__ == "__main__":
    click_btn_by_class_name()