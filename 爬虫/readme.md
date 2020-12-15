# README



sinaNews.py是6.13新浪新闻的爬取样例样例



爬取页面

![](C:\Users\86152\Desktop\大二上\数据科学\大作业\爬虫\新浪滚动新闻.jpg)





爬取代码

```python
import requests                                 #获取网页信息
import json                                     #处理json格式的数据
from bs4 import BeautifulSoup                   #用于数据抽取
import re                                       #正则表达式
from pybloom_live import ScalableBloomFilter    #用于URL去重
import codecs                                   #用于存储爬取信息
import os



# 获取页面中的新闻标题、内容、来源、时间
def getDetailPageBybs(url):
    #通过字典存新闻的这些内容
    detail = {}

    #链接
    detail['url'] = url
    r = requests.get(url)

    #统一编码
    page = r.text.encode(r.encoding).decode(r.apparent_encoding)

    #使用bs抽取数据
    html = BeautifulSoup(page,'lxml')

    #标题
    title = html.find(class_='main-title')
    # print(title.text)
    detail['title'] = title.text

    #内容
    artibody = html.find(class_='article')
    # print(artibody.text)
    detail['artibody'] = artibody.text

    #新闻来源和时间
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

#文本存储
def saveNews(data, title):
    filepath = os.getcwd() + '/新闻1/' + title + '.txt'
    f = open(filepath, 'a+', encoding='utf-8')
    f.write(data)
    f.close()


#使用ScalableBloomFilter模块,对获取的URL去重
urlbloomfilter = ScalableBloomFilter(initial_capacity=100, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)

#存放出错的URL
error_url = set()

#文本存储顺序
sq = ['url', 'title', 'newstime', 'newsfrom', 'artibody']


for page in range(1,153):
    #6月13号的新闻滚动栏网页链接，date对应日期，num对应页面具有的新闻数，page对应页数
    url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&etime=1591977600&stime=1592064000&ctime=1592064000&date=2020-06-13&k=&num=50&page=' + str(page) + '&r=0.924145004402507&callback=jQuery1112004405343527231409_1608012857207&_=1608012857208'
    r = requests.get(url)

    if r.status_code == 200:            #如果请求没问题
        #将动态网页文本以json形式加载为Python字典形式
        reply = json.loads(r.text[47:-14])
        # print(reply['result']['data'][0]['title'])

        #如果网页没有结果跳出循环
        if(len(reply['result']['data']) == 0):
            # print(page)
            break

        #reply['result']['data']是新闻列表上的所有新闻标题及链接
        for i in reply['result']['data']:
            #用re筛选所有标题仅含‘新冠’字符的新闻
            if (re.search(r'新冠',i['title']) is not None) :
                #如果URL没有重复放入去重器
                if i['url'] not in urlbloomfilter:
                    urlbloomfilter.add(i['url'])

                    try:
                        #通过getDetailPageBybs模块得到相应新闻抽取出的数据
                        detail = getDetailPageBybs(i['url'])

                        #字符串构造文本形式
                        data = ''
                        for s in sq:
                            data += (detail[s] + '\n')
                        #文本存储
                        saveNews(data, i['title'])
                    except Exception as e:
                        error_url.add(i['url'])








```

