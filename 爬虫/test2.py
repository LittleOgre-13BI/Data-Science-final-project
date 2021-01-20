
from selenium import webdriver
import time,re,random

browser = webdriver.Chrome()
browser.get('http://weibo.com/')
time.sleep(30)#趁这30秒手动登录微博
sumpage = 12147
fw = open("result1-12147.txt",'a')

for page in range(1,sumpage+1):
    browser.get('http://weibo.cn/breakingnews?page='+str(page))
    html = browser.page_source
    print('PageNumber: '+ str(page))
    fw.write(html+'\n')

    time.sleep(10+random.randint(1,9))#设个随机的时间，不能爬太快
fw.close()