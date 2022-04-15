from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from pprint import pprint

user_email = 'study.ai_172@mail.ru'
user_password = 'NextPassword172#'
# s = Service('./chromedriver')
driver = webdriver.Chrome()
driver.get('https://mail.ru/?from=logout')

#property of driver obj is wait load
driver.implicitly_wait(15)

site_name = driver.title
print(site_name)

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

#Реализация, которая в будущем может работать быстрее, если получится разобраться, как отсортировать ненужные строки. Сейчас голова не варит -_-
# list_mess = []
# href_list = []
# i = 0
# # get href of messages
# while i < 2:
#     #get list of links
#     list_mess = driver.find_elements(By.XPATH, "//div[@class='ReactVirtualized__Grid__innerScrollContainer']/a[contains(@class, 'js-tooltip-direction_letter-bottom')]")
#     last_mess = list_mess[-1].get_attribute('href')
#     if last_mess == list_mess[-1]:
#         break

#     #insert href in href_list
#     for href in list_mess:
#         href_el = href.get_attribute('href')
#         # pprint(href_el)
#         # print(len(href_list))
    
#     #skrolling page
#     actions = ActionChains(driver)
#     actions.move_to_element(list_mess[-1]).perform()
#     time.sleep(4)

#     i +=1 

#     # print(len(href_list))

xpath = "//div[@class='ReactVirtualized__Grid__innerScrollContainer']/a[contains(@class, 'js-tooltip-direction_letter-bottom')]"

links =[]
last_id = None
while True:  # собираем ссылки на новости, прокручивая список
    letters = driver.find_elements(By.XPATH, xpath)  # сканируем все показанные
    l = letters[-1].get_attribute('href')
    if last_id == l:  # список показан полностью - заканчиваем сбор ссылок
        break

    for letter in letters:
        links.append(letter.get_attribute('href').split('?')[0])

    last_id = l
    actions = ActionChains(driver)
    actions.move_to_element(letters[-1]).perform()
    time.sleep(4)

links = list(set(links))  # удаляем дубликаты

