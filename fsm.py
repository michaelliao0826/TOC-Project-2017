from transitions.extensions import GraphMachine
from bs4 import BeautifulSoup

import requests
import time
import os
import re
import urllib.request

PTT_URL = 'https://www.ptt.cc'

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    ## is
    def is_going_to_start(self, update):
        text = update.message.text
        return text.lower() != ''
    
    def is_going_to_user(self, update):
        text = update.message.text
        return text.lower() == 'hi'

    def is_going_to_beauty(self, update):
        text = update.message.text
        return text.lower() == 'beauty'

    def is_going_to_photo(self, update):
        text = update.message.text
        return text.lower() == '1'

    def is_going_to_one(self, update):
        text = update.message.text
        return text.lower() == '2'

    def is_going_to_chat(self, update):
        text = update.message.text
        return text.lower() == 'chat'

    def is_going_to_bath(self, update):
        text = update.message.text
        return text.lower() != ''

    ## on
    def on_enter_start(self, update):
        get_title()
        update.message.reply_text("輸入hi來喚醒我 Zzz")
    
    def on_enter_user(self, update):
        update.message.reply_text("你好，我是聊天機器人Michael\n你可以輸入:\n(1)chat 來跟我聊天\n(2)beauty 來看養眼圖片嘻嘻")
        
    def on_enter_beauty(self, update):
        update.message.reply_text("小色鬼 A_A\n輸入:\n(1)\"1\"，來看很多圖\n(2)\"2\"，一...一張就好...")
        #self.go_back(update)

    def on_enter_photo(self, update):
        update.message.reply_text(str(img_url))
        self.go_back(update)

    def on_enter_one(self, update):
        update.message.reply_text(str(img_url[randint(0, 5)]))
        self.go_back(update)

    def on_enter_bath(self, update):
        update.message.reply_text("我先洗澡等等回")
        self.go_back(update)

    def on_enter_chat(self, update):
        update.message.reply_text("嗨，想跟我聊什麼ㄏㄏ")
        #self.go_back(update)

    # exit
    def on_exit_beauty(self, update):
        print('Leaving state1')
    
    def on_exit_bath(self, update):
        print('Leaving state1')

        
####### beauty serach ########
def get_web_page(url):
    time.sleep(0.5)  # 每次爬取前暫停 0.5 秒以免被 PTT 網站判定為大量惡意爬取
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html.parser')

    # 取得上一頁的連結
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').string.strip() == date:  # 發文日期正確
            # 取得推文數
            push_count = 0
            if d.find('div', 'nrec').string:
                try:
                    push_count = int(d.find('div', 'nrec').string)  # 轉換字串為數字
                except ValueError:  # 若轉換失敗，不做任何事，push_count 保持為 0
                    pass

            # 取得文章連結及標題
            if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                href = d.find('a')['href']
                title = d.find('a').string
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count
                })
    return articles, prev_url


def parse(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    links = soup.find(id='main-content').find_all('a')
    img_urls = []
    for link in links:
        if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
            img_urls.append(link['href'])
    return img_urls

def get_title():
    current_page = get_web_page(PTT_URL + '/bbs/Beauty/index.html')
    global article
    global img_url
    article = []
    img_url = []
    if current_page:
        articles = []  # 全部的今日文章
        date = time.strftime("%m/%d").lstrip('0')  # 今天日期, 去掉開頭的 '0' 以符合 PTT 網站格式
        current_articles, prev_url = get_articles(current_page, date)  # 目前頁面的今日文章
        while current_articles:  # 若目前頁面有今日文章則加入 articles，並回到上一頁繼續尋找是否有今日文章
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, date)

        # 已取得文章列表，開始進入各文章讀圖
        for article in articles:
            print('Processing', article)
            page = get_web_page(PTT_URL + article['href'])
            if page:
                img_url = parse(page)
                article['num_image'] = len(img_url)

    #global info
    #date = time.strftime("%m/%d").lstrip('0')  # 今天日期, 去掉開頭的 '0' 以符合 PTT 網站格式
    #info = get_article(page, date)
    #return info
        
#def get_icons():
#    icon_page = get_web(info[randint(1, 5)]['href'])
#    if icon_page:
#        photo = parse(icon_page)
#    return photo