import os
import re

dirPath = r'C:\Users\86152\Desktop\大二上\数据科学\大作业\爬虫\微博爬取\Selenium'

media = ['澎湃新闻']

for m in media:
    path = dirPath+'/'+m
    os.getcwd()
    dirList = os.listdir(path)
    for dir in dirList:
        childPath = path + '/' + dir
        fileList = os.listdir(childPath)
        for file in fileList:
            fw = open(childPath+'/'+file,'rb')
            text = fw.read()
            try:
                text = text.decode('utf8')
            except Exception:
                text = text.decode('utf8', 'ignore')
            fw.close()
            text = re.subn('\n', '', text)
            comment = re.findall('<comments>(.*?)</comments>',text[0])
            if len(comment) == 0 or comment[0] == '':
                os.remove(childPath+'/'+file)

