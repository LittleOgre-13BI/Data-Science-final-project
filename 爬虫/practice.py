import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://search.sina.com.cn/?q=%E6%96%B0%E5%86%A0&range=title&c=news&sort=time')

r.raise_for_status()

soup = BeautifulSoup(r.text,"html.parser")
box_results = soup.find_all(name='div',attrs={'class':'box-result'})
alist = []
taglist = []
for i in box_results:
    s = str(i.find('h2'))
    x = re.findall(r'fgray_time">(.*?)<',s)
    if(len(x) != 0):
        taglist.append(x[0])
    x = re.findall(r'href="(.*?)"',s)
    if(len(x) != 0):
        alist.append(x[0])

x = 0
for a in alist:
    r = requests.get(a,)
    r.raise_for_status()
    soup = BeautifulSoup(r.text.encode(r.encoding).decode(r.apparent_encoding),"html.parser")
    title = soup.find(name='h1',attrs={'class':'main-title'})
    t = re.findall(r">(.*?)<",str(title))
    if(len(t) > 0):
        f = open(t[0],'w+')
        f.write(t[0]+'\n')
    else:
        f = open('无题','w+')
        f.write('无题'+'\n')
    if(x < len(taglist)):
        f.write('tag:'+taglist[x]+'\n')
    article = soup.find_all(name='p',attrs={'cms-style':'font-L'})
    for i in article:
        f.write(re.sub(r'<(.*?)>','',str(i))+'\n')
    f.close()
    x += 1

