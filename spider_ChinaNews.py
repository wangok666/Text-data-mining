import re
import datetime
from bs4 import BeautifulSoup
import requests
from requests import RequestException
import pymysql
from multiprocessing import Pool


def get_response(url):
    '''
    :param url: 待解析页面的网址
    :return: 页面文本text
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'gbk'
            return response.text
        return None
    except RequestException:
        return None


def get_page_link(html):
    '''
    :param html: 页面文本
    :return: 对解析的每一条url进行文章内容的解析
    '''
    pattern = re.compile(r'<li><div class="dd_lm">.*?>(.*?)</a>]</div> <div class="dd_bt"><a href="(.*?)">(.*?)</a></div><div class="dd_time">.*?</div></li>', re.S)
    datas = re.findall(pattern, html)
    return datas



def insert_sql(label, value):
    '''
    :param label: 类别标签
    :param value: (标题， 文章内容)
    :return: 插入结果
    '''
    db = pymysql.connect("localhost", "root", "123456", "DM")
    cursor = db.cursor()
    topic = {
             '财经': 'cj',
             '港澳': 'ga',
             '国际': 'gj',
             '健康': 'jk',
             '军事': 'js',
             '社会': 'sh',
             '台湾': 'tw',
             '体育': 'ty',
             '文化': 'wh',
             '娱乐': 'yl',
             '汽车': 'qc'
             }
    sql = "INSERT INTO " + topic[label] + '_extra' + "(TITLE,ARTICLE) VALUES (%s, %s)"
    try:
        cursor.execute(sql, value)
        db.commit()
        print('ok')
    except:
        db.rollback()
        print("error")
    db.close()


def parse_datas(datas, label):
    links = []
    topic = {
        '港澳': '/ga/',
        '军事': '/mil/',
        '文化': '/cul/',
        '台湾': '/tw/',
        '娱乐': '/yl/',
        '汽车': '/auto/'
    }
    for data in datas:
        if data[0] == label and data[1].startswith(topic[label]):
            # get_article(data[0], data[1], data[2])
            links.append(data)
    return links

def get_article(article_url):
    '''
    :param article_url: 待解析文章的url
    :param title: 文章标题
    '''
    url = 'http://www.chinanews.com' + article_url
    html = get_response(url)
    try:
        soup = BeautifulSoup(html, 'lxml')
        soup_text = soup.find('div', class_='left_zw')
        if soup_text:
            soup_text = soup_text.text.strip()
            pattern = re.compile(r'\(fun.*?}\)\(\);', re.S)
            text = re.sub(pattern, '', soup_text)
            return text
    except:
        return None


def main(topic):
    now = datetime.datetime.now().date()
    for i in range(365 * 6 + 155):
        now = now + datetime.timedelta(days=-1)
    count = 12198
    print(now.strftime("%Y/%m%d"))
    for i in range(365*3):
        now = now + datetime.timedelta(days=-1)
        print(now.strftime("%Y/%m%d"))
        url = 'http://www.chinanews.com/scroll-news/' + str(now.strftime("%Y/%m%d")) + '/news.shtml'
        html = get_response(url)
        datas = get_page_link(html)
        links = parse_datas(datas, topic)
        for link in links:
            text = get_article(link[1])
            if text:
                value = (link[2], text)
                insert_sql(link[0], value)
                print(topic, count)
                count = count + 1
# # 2015 04 18
# 新文化20150228
# 2015 02 27 40000+

# tw 20140208 35000+

# js 20120429 5951
if __name__ == '__main__':
    # pool = Pool()
    # labels = ['港澳']
    # pool.map(main, [label for label in labels])
    main('娱乐')



    # for i in range(365):
    #     now = now+datetime.timedelta(days=-1)
    #     url = 'http://www.chinanews.com/scroll-news/' + str(now.strftime("%Y/%m%d")) + '/news.shtml'
    #     print(now.strftime("%Y/%m%d"))
        # html = get_response('http://www.chinanews.com/scroll-news/2020/1121/news.shtml')
        # get_page_link(html)
    # html = get_response('http://www.chinanews.com/scroll-news/2020/1121/news.shtml')
    # get_page_link(html)
