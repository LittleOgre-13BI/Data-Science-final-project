import re
import os

dirPath = r'C:\Users\86152\Desktop\大二上\数据科学\大作业\爬虫\微博爬取\Selenium'

media = ['观察者网','凯雷','小满']

for m in media:
    path = dirPath+'/'+m
    os.getcwd()
    dirList = os.listdir(path)
    for dir in dirList:
        childPath = path + '/' + dir
        fileList = os.listdir(childPath)
        for file in fileList:
            state = False
            fw = open(childPath + '/' + file, 'rb')
            text = fw.read()
            try:
                text = text.decode('utf8')
            except Exception:
                text = text.decode('utf8', 'ignore')
            fw.close()

            types = ['source', 'title', 'time', 'url', 'text', 'comments']
            text = re.subn('\n', '', text)
            newText = {}
            for t in types:
                c = re.compile('<' + t + '>(.*?)</' + t + '>')
                temp = c.findall(text[0])
                if len(temp) == 0:
                    print(file)
                    state = True
                else:
                    newText[t] = temp[0]

            if state:
                break
            try:
                comments = newText['comments']
            except Exception:
                print(file)
                break
            comments = re.split('\r', comments)
            for i in range(len(comments)):
                comment = comments[i]
                comment = comment.split('：', 1)
                try:
                    comments[i] = comment[1]
                except Exception:
                    print(file)
                    state = True

            if state:
                break

            newText['comments'] = comments

            fw = open(childPath + '/' + file, 'w',1,'utf8')
            fw.write('<source>' + newText['source'] + '</source>' + '\n<title>' + newText['title'] + '</title>' + '\n<time>' +
                 newText['time'] + '</time>' + '\n<url>' + newText['url'] + '</url>' + '\n\n' + '\n<text>' + newText[
                     'text'] + '</text>' + '\n<comments>'
                 + '\n'.join(newText['comments']) + '</comments>')
            fw.close()

