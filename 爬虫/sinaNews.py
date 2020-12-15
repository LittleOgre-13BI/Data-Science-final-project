import requests                                 #获取网页信息
import json                                     #处理json格式的数据
from bs4 import BeautifulSoup                   #用于数据抽取
import re                                       #正则表达式
from pybloom_live import ScalableBloomFilter    #用于URL去重
import codecs                                   #用于存储爬取信息
import os



# 获取页面中的新闻标题、内容、来源、时间
def getDetailPageBybs(url):
    detail = {}
    detail['url'] = url
    r = requests.get(url)
    page = r.text.encode(r.encoding).decode(r.apparent_encoding)
    html = BeautifulSoup(page,'lxml')
    title = html.find(class_='main-title')
    # print(title.text)
    detail['title'] = title.text
    artibody = html.find(class_='article')
    # print(artibody.text)
    detail['artibody'] = artibody.text
    date_source = html.find(class_='date-source')
    if date_source.a:
        # print(date_source.span.text)
        detail['newstime'] = date_source.span.text
        # print(date_source.a.text)
        detail['newsfrom'] = date_source.a.text
    else:
        detail['newstime'] = date_source('span')[0].text
        detail['newsfrom'] = date_source('span')[1].text

    return detail

def saveNews(data, title):
    filepath = os.getcwd() + '/新闻1/' + title + '.txt'
    f = open(filepath, 'a+', encoding='utf-8')
    f.write(data)
    f.close()




#使用ScalableBloomFilter模块,对获取的URL去重
urlbloomfilter = ScalableBloomFilter(initial_capacity=100, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
error_url = set()
sq = ['url', 'title', 'newstime', 'newsfrom', 'artibody']


for page in range(1,153):
    url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&etime=1591977600&stime=1592064000&ctime=1592064000&date=2020-06-13&k=&num=50&page=' + str(page) + '&r=0.924145004402507&callback=jQuery1112004405343527231409_1608012857207&_=1608012857208'
    r = requests.get(url)
    if r.status_code == 200:
        reply = json.loads(r.text[47:-14])
        # print(reply['result']['data'][0]['title'])
        if(len(reply['result']['data']) == 0):
            # print(page)
            break
        for i in reply['result']['data']:
            if (re.search(r'新冠',i['title']) is not None) :
                if i['url'] not in urlbloomfilter:
                    urlbloomfilter.add(i['url'])
                    try:
                        detail = getDetailPageBybs(i['url'])
                        data = ''
                        for s in sq:
                            data += (detail[s] + '\n')
                        saveNews(data, i['title'])
                    except Exception as e:
                        error_url.add(i['url'])







