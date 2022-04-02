from bs4 import BeautifulSoup as bs 
import requests
from pprint import pprint

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

def get_dict_vac(dom, base_url): 
    """Получаем словарь с инфой о предложениях"""
    vacancies = dom.find_all('div', {'class':'vacancy-serp-item'})
    vacancies_data = {}
    numb = 1

    for vac in vacancies:
        
        vac_link_a = vac.find('a', {'class':'bloko-link'})
        vac_name = vac_link_a.getText()
        vac_link = vac_link_a['href']
        vac_site = base_url

        try:
            salary = vac.find('span', {'class':'bloko-header-section-3'}).getText()
            vac_salary = get_salary(salary)
        except:
            vac_salary = get_salary(False)

        vacancies_data[f'v_{numb}'] = {'vac_name' : vac_name, 'vac_salary' : vac_salary, 'vac_link' : vac_link, 'vac_site' : vac_site}
        
        numb +=1
    if vacancies_data:
        return vacancies_data
    else: 
        print('По запросу ничего не найдено')

def get_url_for_search_work(search_text, page = 0):
    """Получаем ссылку на поиск вакансий по запросу"""
    base_url = 'https://rostov.hh.ru'

    if page == 0:
        search_page = f'{base_url}/search/vacancy?area=76&fromSearchLine=true&text={search_text}'
    else: 
        search_page = f'{base_url}/vacancies/{search_text}?page={page}&hhtmFrom=vacancy_search_catalog'

    user_headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
    
    return [search_page, user_headers, base_url]

if __name__ == '__main__':
    search_text = input('Введите желаемую должность: ').replace(' ', '+')  #'data+dev'
    url = get_url_for_search_work(search_text)
    response_site = requests.get(url[0], headers=url[1])

    dom = bs(response_site.text, 'html.parser')
    val_pages = get_val_pages(dom)
    vac_dict = {}

    if val_pages > 0:
        user_page = input(f'По данному запросу есть {val_pages} стр, какую откроем? Введите число от 1 до {val_pages}: ')
        url = get_url_for_search_work(search_text, user_page)
        vac_dict = get_dict_vac(dom, url[2])
    else: 
        vac_dict = get_dict_vac(dom, url[2])

    if vac_dict:
        pprint(vac_dict)
    else:
        print('Похоже Вы ошиблись при вводе, попробуйте еще раз')