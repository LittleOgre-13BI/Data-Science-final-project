import requests
import re
from bs4 import BeautifulSoup as bs

userList = []
pageNum = 1
while len(userList) < 50:
    r = requests.get('https://s.weibo.com/user?q=%E6%96%B0%E9%97%BB&Refer=weibo_user&page='+str(pageNum))
    page = r.text.encode(r.encoding).decode(r.apparent_encoding)

    html = bs(page,'lxml')

    userPage = html.findAll(class_='name')

    for item in userPage:
        user = {}
        url = re.findall(r'href="(.*?)"',str(item))
        user['url'] = 'https:'+url[0]
        name = re.findall(r'[\u4e00-\u9fa5]',str(item))
        user['name']=''.join(name)
        userList.append(user)

    pageNum += 1

fw = open("userList.text",'a')
for user in userList:
    fw.write(user['name']+'<:>')
    fw.write(user['url']+'\n')

fw.close()