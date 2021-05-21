import requests
from bs4 import BeautifulSoup
from requests import RequestException
import multiprocessing
import threading
import re
import pymysql

index = 1
def get_response(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf8'
            return response.text
        return None
    except RequestException:
        return None

def get_links(html):
    pattern = re.compile(r'<li><.*?href="(.*?)".*?_blank">(.*?)</a><span>(.*?)</span>', re.S)
    datas = re.findall(pattern, html)
    for data in datas:
        get_news(data[0])

def get_news(link):
    html = get_response(link)
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('.main-title')
    if not title:
        title = soup.select('#artibodyTitle')
    if title:
        title = title[0].text

    date = soup.select('.date')
    if not date:
        date = soup.select('#pub_date')
    if date:
        date = date[0].text

    # 正文
    articles = soup.select('div[class="article"] p')
    if not articles:
        article = soup.select('div[id="artibody"] p')
    if articles:
        # 把正文放在一个列表中 每个p标签的内容为列表的一项
        article_str = ''
        for article in articles:
            article_str = article_str + str(article.text).strip()

        # print(link)
        # print(title)
        # print(article_str)
        value = (title, date, article_str, link)
        insert(value)
        print(value[0])


def insert(value):
    db = pymysql.connect("localhost", "root", "123456", "DM")

    cursor = db.cursor()
    sql = "INSERT INTO DOMESTIC(TITLE,DATE,ARTICLE,LINK) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(sql, value)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print("插入数据失败")
    db.close()


def main(page):
    print(page)
    url = 'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_' + str(page) + '.shtml'
    text = get_response(url)
    get_links(text)


if __name__ == '__main__':
    for i in range(1, 1001):
        main(i)



