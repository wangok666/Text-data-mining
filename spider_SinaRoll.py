from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from requests import RequestException
import time
from selenium.common.exceptions import NoSuchElementException
import pymysql


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


def get_page_links():
    news = browser.find_elements_by_xpath('//div[@class="d_list_txt"]/ul/li/span/a')
    for new in news:
        link = new.get_attribute('href')
        get_news(link)


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
            article_str = article_str + str(article.text)

        # print(link)
        # print(title)
        # print(article_str)
        value = (title, date, article_str, link)
        insert(value)
    # news = {'link': link, 'title': title, 'date': date, 'article': article_str}
    # print(news)


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


if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get('https://news.sina.com.cn/roll/#pageid=153&lid=2510&k=&num=50&page=1')
    get_page_links()
    # while True:
    # 新浪滚动新闻爬取50页
    for i in range(1, 51):
        try:
            browser.find_element_by_xpath('//a[@onclick="newsList.page.next();return false;"]').click()
            time.sleep(1)
            get_page_links()
        except NoSuchElementException:
            print('Can not find the next page button')
            browser.close()
            break

