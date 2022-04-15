
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from time import sleep


options = Options()
options.add_argument("start-maximized")

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)


# === авторизация ===
driver.get('https://account.mail.ru/login')

# логин
elem = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
elem.send_keys("study.ai_172@mail.ru")
elem.send_keys(Keys.ENTER)

# пароль
elem = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
sleep(1)  # не знаю как по-другому сделать
elem.send_keys("NextPassword172#")
elem.send_keys(Keys.ENTER)


# === сбор ссылок на письма из общего списка ===
links = []  # ссылки на страницы детального просмотра сообщений

xpath = "//a[contains(@href,'/inbox/0:')]"  # строка с анонсом письма
_ = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))  # ждём

last_id = None
while True:  # собираем ссылки на новости, прокручивая список
    letters = driver.find_elements(By.XPATH, xpath)  # сканируем все показанные
    l = letters[-1].get_attribute('href')
    print(l)
    if last_id == l:  # список показан полностью - заканчиваем сбор ссылок
        break

    for letter in letters:
        links.append(letter.get_attribute('href').split('?')[0])

    last_id = l
    actions = ActionChains(driver)
    actions.move_to_element(letters[-1]).perform()
    sleep(4)

links = list(set(links))  # удаляем дубликаты


# === сканирование страниц детального просмотра, получение данных письем ===
data = []  # список словарей с данными писем

for link in links:
    driver.get(link)
    # весь интерфейс грузится фоновыми запросами, поэтому сначала ожидаем
    _ = wait.until(EC.presence_of_element_located((By.XPATH,"//h2[@class='thread-subject']")))

    sleep(5)

    h2 = wait.until(EC.presence_of_element_located((By.XPATH,"//h2[@class='thread-subject']"))).get_attribute("innerText")

    frm = wait.until(EC.presence_of_element_located((By.XPATH,"//span[@class='letter-contact']"))).get_attribute("title")

    date = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='letter__date']"))).get_attribute("innerText")

    text = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='letter__body']"))).get_attribute("innerText")

    el = {}
    el['from'] = frm  # от кого,
    el['date'] = date  # дата отправки,
    el['topic'] = h2  # тема письма,
    el['text'] = text.replace('\n', ' ').replace('\t', ' ')  # текст письма

    data.append(el)


# # === сохраняем результаты в базу ===
# client = MongoClient('127.0.0.1', 27017)  # соединение
# mongodb = client['letters']  # база
# lettersdb = mongodb.lettersdb  # коллекция

# for el in data:
#     try:
#         # el['_id'] = el['id']  # в будущем тут стоит поставить id письма
#         lettersdb.insert_one(el)
#     except Exception as e:
#         print('Ошибка при сохранении новости в базу:')
#         print(e)