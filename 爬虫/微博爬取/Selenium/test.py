import re
import os

fw = open(r'C:\Users\86152\Desktop\大二上\数据科学\大作业\爬虫\微博爬取\Selenium\新浪新闻\202006\202006251003.txt','rb')
text = fw.read()
try:
    text = text.decode('utf8')
except Exception:
    text = text.decode('utf8', 'ignore')
fw.close()
text = re.subn('\n','',text)

comment = re.findall(r'<comments>(.*?)</comments>',text[0])
print(comment)
comment = re.split('\r',comment[0])
print(comment)
