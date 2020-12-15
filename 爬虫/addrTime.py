import requests
from bs4 import BeautifulSoup
import re
import sys

def Next(text):
    page = BeautifulSoup(text,"html.parser")
    nextPage = page.find_all(name='a',attrs={'class':'n'})
    if(len(nextPage) > 1):
        u =  'http://www.baidu.com' + re.findall(r'href="(.*?)"', str(nextPage[1]))[0]
    else:
        print(nextPage)
        print('\n')
        print(url)
        sys.exit(0)
    u = re.sub(r'amp;','',u)
    return u


def CheckTime(text):
    page = BeautifulSoup(text,"html.parser")
    firstNew = page.find(name='div',attrs={'class':'news-source'})
    tag = firstNew.find_all(name='span')
    time =  re.findall(r'年(.*?)日',str(tag))
    time = re.split(r'月',time[0])
    print(time[0],'  ',type(time[0]))
    if(time[0] == '6'):
        print(url)
    else:
        return False


    # for i in firstNew:
    #     tag = i.find_all(name='span')
    #     print(len(tag))

    # tag = firstNew.find(name='span',attrs={'class':'fgray_time'})

    # time = re.findall(r'\d\d\d\d-\d\d-\d\d',str(tag))
    # print(time[0])

# news = page.find_all(name='a',attrs={'class':'news-title-font_1xS-F'})
# print()

def access(ur):
    req = requests.get(ur)
    req.raise_for_status()
    return req.text

url = 'http://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E6%96%B0%E5%86%A0&medium=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.000000&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn=50'
text = access(url)
while not CheckTime(text):
    text = access(url)
    url = Next(text)

