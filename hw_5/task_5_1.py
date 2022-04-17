from http import client
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from pprint import pprint
from pymongo import MongoClient
from datetime import date

user_email = 'study.ai_172@mail.ru'
user_password = 'NextPassword172#'
# s = Service('./chromedriver')
driver = webdriver.Chrome()
driver.get('https://mail.ru/?from=logout')

#property of driver obj is wait load
driver.implicitly_wait(15)

#get site name
site_url = driver.title
site_name = site_url.split(':')[0]

def find_elem(el_xpath):
    elem = driver.find_element(By.XPATH, el_xpath)
    return elem

#log_in
find_elem("//div[contains(@class, 'logged-out-one-click')]/button").click()

#get form
driver.get(find_elem("//iframe[@class='ag-popup__frame__layout__iframe']").get_attribute('src'))

#send email
find_elem("//div[@class='base-0-2-57']/div/div/input").send_keys(user_email)
find_elem("//button[@class='base-0-2-79 primary-0-2-93']").send_keys(Keys.ENTER)

#send password
find_elem("//input[contains(@class,'withIcon-0-2-72')]").send_keys(user_password)
find_elem("//div[@class='submit-button-wrap']/*/button").send_keys(Keys.ENTER)

dict_mess_links = {}
last_id = "none"
# get href of messages
while True:
    #get list of links
    list_mess = driver.find_elements(By.XPATH, "//div[@class='ReactVirtualized__Grid__innerScrollContainer']/a[contains(@class, 'js-tooltip-direction_letter-bottom')]")
    last_href_in_list = str(str(list_mess[-1].get_attribute('href')).split(':')[2])
    
    #insert href in dict_mess_links
    for href in list_mess:
        href_el = href.get_attribute('href')
        uniq_id = str(href_el.split(':')[2])

        if dict_mess_links.get(uniq_id, 'none') != uniq_id:
            dict_mess_links[uniq_id] = {"id" : uniq_id, 'link' : href_el}
    
    #skrolling page
    actions = ActionChains(driver)
    actions.move_to_element(list_mess[-1]).perform()
    time.sleep(4)
    print(len(dict_mess_links))
    if last_id == last_href_in_list:
        break
    else:
        last_id = last_href_in_list


# client = MongoClient('127.0.0.1', 27017)
# db = client[site_name]
# emails = db.emails

# for link in links:
#     driver.get(link)
#     time.sleep(4)

#     # от кого, дата отправки, тема письма, текст письма полный
#     from_user = find_elem("//span[@class='letter-contact']").get_attribute('title')

#     mess_date = find_elem("//div[@class='letter__date']").text
#     today = date.today()
#     yesturday = f"{today.year}-{today.month}-{today.day - 1}"
#     mess_date = mess_date.replace("Сегодня", str(today))
#     mess_date = mess_date.replace("Вчера", yesturday)

#     theme = find_elem("//h2[@class='thread-subject']").text

#     mess_text = find_elem("//div[@class='letter-body']").text

#     doc = {
#         "_id" : f"{site_name}_{from_user}_{mess_date}",
#         "site_url" : site_url,
#         "from_user" : from_user,
#         "date" : mess_date,
#         "theme" : theme,
#         "mess_text" : mess_text
#     }
