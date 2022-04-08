from bs4 import BeautifulSoup as bs 
import requests
from pprint import pprint
from pymongo import MongoClient as MC
import re

def get_salary(salary):
    if salary == False:
        return {'min' : None, 'max': None, 'currensy': None}

    salary = salary.replace('\u202f', '')
    salary = salary.split(' ')

    if salary[0] == 'от':
        salary_min = int(salary[1])
        salary_max = None
    elif salary[0] == 'до':
        salary_min = None
        salary_max = int(salary_min = salary[1])
    else:
        salary_min = int(salary[0])
        salary_max = int(salary_min = salary[2])

    salary_currensy = salary[len(salary) - 1]
    salary = {'min' : salary_min, 'max': salary_max, 'currensy': salary_currensy}

    return salary

def get_val_pages(dom):
    try:
        parent_pages = dom.find('div', {'class':'pager'}).findChildren(recursive=False)
        span_last_pages = parent_pages[len(parent_pages) - 2]
        val_pages = int(span_last_pages.find('a').find('span').text)
    except:
        val_pages = 0
    
    return val_pages

def add_new_vac(dom, base_url, page, db_name, key_word): 
    """Получаем словарь с инфой о предложениях"""
    all_vacancies = dom.find_all('div', {'class':'vacancy-serp-item'})
    vacs = connect_db(db_name).vacancies

    for vac in all_vacancies:
        try:
            vac_link_a = vac.find('a', {'class':'bloko-link'})
            vac_name = vac_link_a.getText()
            vac_link = vac_link_a['href']
            vac_id = re.compile(r'[\/]\d*[\?]').findall(vac_link)[0][1:-1]

            try:
                salary = vac.find('span', {'class':'bloko-header-section-3'}).getText()
                vac_salary = get_salary(salary)
            except:
                vac_salary = get_salary(False)

            doc = { "_id" : vac_id, "vac_name" : vac_name, "vac_site" : base_url, "vac_link" : vac_link, "vac_salary" : vac_salary, "page" : page, "key_word" : key_word}
            vac_id = vacs.find_one({"_id" : doc["_id"]})

            if not vac_id:
                vacs.insert_one(doc)
        except:
            pass


def get_url_for_search_work(search_text, page = 0):
    """Получаем ссылку на поиск вакансий по запросу"""
    base_url = 'https://rostov.hh.ru'

    if page == 0:
        search_page = f'{base_url}/search/vacancy?area=76&fromSearchLine=true&text={search_text}'
    else: 
        page = page - 1
        search_page = f'{base_url}/vacancies/{search_text}?page={page}&hhtmFrom=vacancy_search_catalog'

    user_headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
    
    return [search_page, user_headers, base_url]

def connect_db(db_name):
    client = MC('127.0.0.1', 27017)
    db = client[db_name]
    # не нашла способ проверить подключение к бд.

    return db

def get_dom(search_text, val_page = 0):
    url = get_url_for_search_work(search_text, val_page)
    response_site = requests.get(url[0], headers=url[1])
    dom = bs(response_site.text, 'html.parser')

    return dom

def get_vac_with_salary(db, wish_salary, key_word):
    vacs = connect_db(db).vacancies
    vac_list = []

    # doc = vacs.find({'$or': [
    #     {'key_word' : key_word, 'vac_salary'['min'] : {'$gte': wish_salary}}, 
    #     {'key_word' : key_word, 'vac_salary'['max'] : {'$lte': wish_salary}}
    # ]})

    for d in vacs.find({'key_word' : key_word}): #, 'vac_salary': {"$gt" : wish_salary}
        #Не нашла способоа лучше.
        
        salary_min = d['vac_salary']['min']
        salary_max = d['vac_salary']['max']
    
        try:
            if salary_min >= wish_salary or salary_max <= wish_salary:
                vac_list.append(d)
        except:
            print("Ищем подходящую вакансию по запросу")
    
    return vac_list


if __name__ == '__main__':
    err_message = 'Похоже Вы ошиблись при вводе, попробуйте еще раз'
    search_text = input('Введите желаемую должность: ').replace(' ', '+')  #'data+dev'
    val_pages = get_val_pages(get_dom(search_text))
    i = 1

    while val_pages >= i:
        print(f'Wait. {i} from {val_pages}')
        url = get_url_for_search_work(search_text, i)
        add_new_vac(get_dom(search_text, i), url[2], val_pages, 'work', search_text)
        i += 1

    try:
        wish_salary = int(input('Введите желаемую зп: '))
        vacs = get_vac_with_salary('work', wish_salary, search_text)
        pprint(vacs)
    except:
        print(err_message)