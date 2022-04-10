from lxml import html
import requests
from pymongo import MongoClient
from pprint import pprint

url = 'https://lenta.ru/'
header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}

resp = requests.get(url, headers = header)
dom = html.fromstring(resp.text)
client = MongoClient('127.0.0.1', 27017)

db = client['news']
top_new_list = dom.xpath("//a[contains(@class, '_topnews')]")
top_news = []

for new in top_new_list:
    news_info = {}

    news_name = new.xpath(".//div[contains(@class, '__title') or contains(@class, 'card-mini__text')]/*/text()")[0]
    news_link = url + new.xpath(".//../@href")[0]
    news_time = new.xpath(".//div/time/text()")[0]

    # название источника;
    # наименование новости;
    # ссылку на новость;
    # дата публикации.
    news_info['source'] = url
    news_info['name'] = news_name
    news_info['link'] = news_link
    news_info['time'] = news_time
    
    top_news.append(news_info)

lenta = db.lenta
lenta.drop()
lenta.insert_many(top_news)

for doc in lenta.find({}):
    pprint(doc)