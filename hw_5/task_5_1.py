from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

user_email = 'study.ai_172@mail.ru'
user_password = 'NextPassword172#'
# s = Service('./chromedriver')
driver = webdriver.Chrome()
driver.get('https://mail.ru/?from=logout')

site_name = driver.title
print(site_name)

def find_elem(el_xpath):
    elem = driver.find_element(By.XPATH, el_xpath)
    return elem

#log_in_
find_elem("//div[contains(@class, 'logged-out-one-click')]/button").click()

#get form
driver.get(find_elem("//iframe[@class='ag-popup__frame__layout__iframe']").get_attribute('src'))
time.sleep(.5)

#send email
find_elem("//div[@class='base-0-2-57']/div/div/input").send_keys(user_email)
find_elem("//button[@class='base-0-2-79 primary-0-2-93']").send_keys(Keys.ENTER)
time.sleep(.5)

#send password
find_elem("//input[contains(@class,'withIcon-0-2-72')]").send_keys(user_password)
find_elem("//div[@class='submit-button-wrap']/*/button").send_keys(Keys.ENTER)
time.sleep(.5)

#STOP_POINT
# list_mess = driver.find_element(By.XPATH, "//div[@class='ReactVirtualized__Grid__innerScrollContainer']/a").get_attribute('href') #.__getattribute__('href')
# for href in list_mess:
#     pass
# time.sleep(.5)
# print(list_mess)

driver.quit()
# input = "//div[contains(@class,'ag-popup__frame__layout-desktop')]"
# elem = driver.find_element(By.ID,)