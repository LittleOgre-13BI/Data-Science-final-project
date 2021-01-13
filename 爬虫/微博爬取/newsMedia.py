import requests
from bs4 import BeautifulSoup as bs
import re


pageNum = 1
r = requests.get('https://s.weibo.com/user?q=%E6%96%B0%E9%97%BB&Refer=weibo_user&page='+str(pageNum))
page = r.text.encode(r.encoding).decode(r.apparent_encoding)
html = bs(page,'lxml')
name = html.findAll(class_='name')

mediaList = []

media = {}

media['url'] = re.findall(r'href="(.*?)"')




