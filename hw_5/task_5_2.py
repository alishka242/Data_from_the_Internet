from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

# s = Service('./chromedriver')
driver = webdriver.Chrome()
driver.get('https://mail.ru/?from=logout')


def find_elem(el_xpath):
    elem = driver.find_element_by_xpath(el_xpath)
    return elem

user_email = 'study.ai_172@mail.ru'
user_password = 'NextPassword172#'

#log_in_
elem = "//div[contains(@class, 'logged-out-one-click')]/button"
find_elem(elem).click()

#get form
elem = find_elem("//iframe[@class='ag-popup__frame__layout__iframe']").get_attribute('src')
driver.get(elem)
time.sleep(.5)

#find input-el and send email
elem = find_elem("//div[@class='base-0-2-57']/div/div/input").send_keys(user_email)
button = find_elem("//button[@class='base-0-2-79 primary-0-2-93']").send_keys(Keys.ENTER)
time.sleep(.5)

#find input-el and send password, and also log in
elem = find_elem("//input[contains(@class,'withIcon-0-2-72')]").send_keys(user_password)
button = find_elem("//div[@class='submit-button-wrap']/*/button").send_keys(Keys.ENTER)


# list_mess = driver.find_elements_by_xpath("//div[@class='ReactVirtualized__Grid__innerScrollContainer']/a") #.__getattribute__('href')
# time.sleep(.5)
# print(type(list_mess))



# input = "//div[contains(@class,'ag-popup__frame__layout-desktop')]"
# elem = driver.find_element(By.ID,)