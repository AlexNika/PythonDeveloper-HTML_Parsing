from lxml import html
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from datetime import datetime
from tabulate import tabulate
import requests
import pandas as pd
import time


def lr_news_time_convert(news_date):
    news_date = news_date.lstrip().split(',')
    news_date[1] = news_date[1].lstrip().split()
    news_date[1][1] = MONTHS.get(news_date[1][1])
    news_date[1] = '-'.join(news_date[1])
    news_date.reverse()
    return ' '.join(news_date)


def mr_news_time_convert(news_date):
    news_date = news_date.replace('T', ' ')
    _i = news_date.rfind('+')
    return news_date[0:_i]


def mn_news_time_convert(news_date):
    news_date = news_date.lstrip().split(' ')
    news_date[0] = news_date[0].split('.')
    _year = str(datetime.today().year)
    news_date[0] = f'{_year}-{news_date[0][1]}-{news_date[0][0]}'
    return f'{news_date[0]} {news_date[1]}:00'


MONTHS = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
          'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}
HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/77.0.3865.120 Safari/537.36'}
PAUSE = 0.25
mr_df = pd.DataFrame()
lr_df = pd.DataFrame()
mn_df = pd.DataFrame()

mailRU_url = 'https://mail.ru'
mr_news_url = []
mr_news_text = []
mr_news_time = []
mr_request = requests.get(mailRU_url, headers=HEADER)
if mr_request.status_code == 200:
    mr_html = mr_request.text
    parsed_html = bs(mr_html, 'lxml')
    class_list = ['news-item_main', 'news-item_inline-first', 'news-item_inline']
    mr_news = parsed_html.find_all('div', class_=class_list)
    for news in mr_news:
        _url = news.find('a').get('href')
        base_url = urlparse(_url)
        if base_url.netloc != f'news.{mailRU_url[8:]}':
            continue
        news_request = requests.get(_url, headers=HEADER)
        if news_request.status_code == 200:
            news_html = news_request.text
            parsed_1news_html = bs(news_html, 'lxml')
            mr_news_text.append(parsed_1news_html.find('h1', {'class': 'hdr__inner'}).getText())
            _time = parsed_1news_html.find('span', {'class': 'js-ago'})['datetime']
            _time = datetime.strptime(mr_news_time_convert(_time), '%Y-%m-%d %H:%M:%S')
            mr_news_time.append(_time)
        time.sleep(PAUSE)
        mr_news_url.append(_url)

    mailRU_news = {'Source': mailRU_url[8:], 'News Title': mr_news_text, 'News URL': mr_news_url,
                   'News time': mr_news_time}
    mr_df = pd.DataFrame(data=mailRU_news)
    mr_df.index = mr_df['News time']
    mr_df.drop('News time', axis=1, inplace=True)
    # print(tabulate(mr_df, headers='keys', tablefmt='psql'))

lentaRU_url = 'https://lenta.ru'
lr_request = requests.get(lentaRU_url, headers=HEADER)
if lr_request.status_code == 200:
    parsed_html = html.fromstring(lr_request.text)
    lr_news_urls = parsed_html.xpath('//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]\
    /h2/a/@href | //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"]/a/@href')
    lr_news_text = parsed_html.xpath('//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]\
    /h2/a/text() | //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"]/a/text()')
    lr_news_time = parsed_html.xpath('//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]\
    /h2/a/time/@datetime | //section[@class="row b-top7-for-main js-top-seven"]\
    //div[@class="item"]/a/time/@datetime')
    for i in range(len(lr_news_urls)):
        if lr_news_urls[i][0] == '/':
            lr_news_urls[i] = lentaRU_url + lr_news_urls[i]
    for i in range(len(lr_news_time)):
        lr_news_time[i] = lr_news_time_convert(lr_news_time[i])
        lr_news_time[i] = datetime.strptime(lr_news_time[i], '%d-%m-%Y %H:%M')

    lentaRU_news = {'Source': lentaRU_url[8:], 'News Title': lr_news_text, 'News URL': lr_news_urls,
                    'News time': lr_news_time}
    lr_df = pd.DataFrame(data=lentaRU_news)
    lr_df.index = lr_df['News time']
    lr_df.drop('News time', axis=1, inplace=True)
    # print(tabulate(lr_df, headers='keys', tablefmt='psql'))

mignewsCOM_url = 'http://mignews.com'
mn_news_url = []
mn_news_text = []
mn_news_time = []
mn_request = requests.get(mignewsCOM_url, headers=HEADER)
if mn_request.status_code == 200:
    mn_html = mn_request.text
    parsed_html = bs(mn_html, 'lxml')
    mn_news = parsed_html.find_all('div', {'class': 'lenta'})
    for news in mn_news:
        _url = news.find('a', {'class': 'time2'}).get('href')
        _url = f'{mignewsCOM_url}{_url}'
        news_request = requests.get(_url, headers=HEADER)
        if news_request.status_code == 200:
            news_html = news_request.text
            parsed_1news_html = bs(news_html, 'lxml')
            mn_news_text.append(parsed_1news_html.find('h1').getText())
            _time = parsed_1news_html.find('span', {'class': 'txtm'}).getText()
            _time = datetime.strptime(mn_news_time_convert(_time), '%Y-%m-%d %H:%M:%S')
            mn_news_time.append(_time)
            time.sleep(PAUSE)
        mn_news_url.append(_url)

    mignewsCOM_news = {'Source': mignewsCOM_url[7:], 'News Title': mn_news_text, 'News URL': mn_news_url,
                       'News time': mn_news_time}
    mn_df = pd.DataFrame(data=mignewsCOM_news)
    mn_df.index = mn_df['News time']
    mn_df.drop('News time', axis=1, inplace=True)
    # print(tabulate(mn_df, headers='keys', tablefmt='psql'))

df_NEWS = pd.DataFrame()
if not mr_df.empty:
    df_NEWS = pd.concat([df_NEWS, mr_df])
if not lr_df.empty:
    df_NEWS = pd.concat([df_NEWS, lr_df])
if not mn_df.empty:
    df_NEWS = pd.concat([df_NEWS, mn_df])
print(tabulate(df_NEWS, headers='keys', tablefmt='psql'))
