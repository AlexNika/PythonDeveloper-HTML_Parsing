from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
import random
import os
import pickle
import telebot
from telebot import apihelper


def check_date(_date):
    try:
        _year, _month, _day = _date.split('-')
        _year = int(_year)
        _month = int(_month)
        _day = int(_day)
    except ValueError:
        return False
    try:
        _valid_date = datetime(year=_year, month=_month, day=_day)
    except ValueError:
        return False
    if datetime(year=2002, month=1, day=1) < _valid_date <= datetime.now():
        return True
    else:
        return False


class Site:
    def __init__(self, _url):
        self.header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/77.0.3865.120 Safari/537.36'}
        self.url = _url
        self.parsed_html = bs(features='lxml')

    def do_request(self, _url):
        self.url = _url
        _result = requests.get(self.url, headers=self.header)
        if _result.status_code == 200:
            _result = _result.text
            self.parsed_html = bs(_result, features='lxml')
            return 200
        else:
            return _result.status_code

    def do_process1(self):
        news_links = []
        news_date_time = []
        news_title = []
        _links = self.parsed_html.find_all('a', {'class': 'news-container-item'})
        _titles = self.parsed_html.find_all('span', {'class': 'news-container-item__article-title'})
        for _link, _title in zip(_links, _titles):
            news_links.append(_link.get('href'))
            _attrs = _link.attrs
            news_date_time.append(_attrs['data-time'])
            news_title.append(_title.getText().replace('\n', '').strip())
        total_news = len(news_links)
        return total_news, news_date_time, news_title, news_links


MAIN_URL = 'https://regnum.ru/news/search/'
TOKEN = '986796592:AAGO79OpINE4BbUgu8enh3pEKmdgcq6Kakc'
PROXIES = {'http': 'http://85.132.71.82:3128',
           'https': 'http://85.132.71.82:3128'}

apihelper.proxy = PROXIES

regnum_ru = Site(MAIN_URL)
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if os.path.exists('greetings.pkl'):
        with open('greetings.pkl', 'rb') as f:
            greetings = pickle.load(f)
        f.close()
    else:
        greetings = ['Доброго времени суток!', 'Привет!']

    bot.reply_to(message, random.choice(greetings))


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = '''
    Команды, которые помогут нам пообщаться:
    /start - Приветственное сообщение 
    /help - Финансововую помощь не окажу, но разобраться в том, что здесь происходим помогу. Читай команды дальше...
    /getnews YYYY-MM-DD N - появятся новости на конкретную дату. Формат даты обязателен - 'YYYY-MM-DD'.
    Если параметр N не задан, то по умолчанию выведется 5 первых новостей.
    /now N - появятся сегодняшние новости. Если параметр N не задан, то по умолчанию выведется 5 первых новостей. 
    "слово" - любое осмысленное слово, по которому хочется найти новости. Пока допустимо только одно слово.
    Внимание! Выводятся все найденные новости по заданному слову.
    '''
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['now'])
def send_now(message):
    _number_news = 5
    _search_date = datetime.today().strftime('%Y-%m-%d')
    args = message.text.split(' ')[1:]
    if len(args) == 1:
        try:
            _number_news = int(args[0])
        except ValueError:
            bot.reply_to(message, 'Упс.. Что-то не то ввели. Я выведу только первые 5 новостей')
    elif len(args) > 1:
        bot.reply_to(message, 'Упс.. Что-то не то ввели. Я выведу только первые 5 новостей')
    _url = f'{MAIN_URL}{_search_date}.html'
    status_code = regnum_ru.do_request(_url)
    if status_code == 200:
        _total_news, _news_date_time, _news_title, _news_links = regnum_ru.do_process1()
        if _number_news > _total_news:
            _number_news = _total_news
        i = 0
        for _link, _title in zip(_news_links, _news_title):
            if i <= _number_news - 1:
                _text = f'{_title}\n{_link}'
                bot.send_message(message.chat.id, _text, disable_web_page_preview=True)
                i += 1
            else:
                break


@bot.message_handler(commands=['getnews'])
def send_getnews(message):
    _number_news = 5
    _search_date = datetime.today().strftime('%Y-%m-%d')
    args = message.text.split(' ')[1:]
    if len(args) == 1:
        if check_date(args[0]):
            _search_date = args[0]
        else:
            bot.reply_to(message, 'Упс.. Что-то не то ввели. Я найду сегодняшние новости и выведу первые 5')
    elif len(args) >= 2:
        if check_date(args[0]):
            _search_date = args[0]
        else:
            bot.reply_to(message, 'Упс.. Что-то не то ввели. Я найду сегодняшние новости')
        try:
            _number_news = int(args[1])
        except ValueError:
            bot.reply_to(message, 'Упс.. Что-то не то ввели. Я выведу только первые 5 новостей')
    _url = f'{MAIN_URL}{_search_date}.html'
    status_code = regnum_ru.do_request(_url)
    if status_code == 200:
        _total_news, _news_date_time, _news_title, _news_links = regnum_ru.do_process1()
        if _number_news > _total_news:
            _number_news = _total_news
        i = 0
        for _link, _title in zip(_news_links, _news_title):
            if i <= _number_news - 1:
                _text = f'{_title}\n{_link}'
                bot.send_message(message.chat.id, _text, disable_web_page_preview=True)
                i += 1
            else:
                break


@bot.message_handler(content_types=['text'])
def find_text(message):
    _search_text = message.text.split(' ')[0]
    _url = f'{MAIN_URL}{_search_text}.html'
    status_code = regnum_ru.do_request(_url)
    if status_code == 200:
        _total_news, _news_date_time, _news_title, _news_links = regnum_ru.do_process1()
        for _link, _title in zip(_news_links, _news_title):
            _text = f'{_title}\n{_link}'
            bot.send_message(message.chat.id, _text, disable_web_page_preview=True)


bot.polling()
