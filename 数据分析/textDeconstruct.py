import re

'''
    @:param path
    @:return newText,字典形式，keys:source,title,time,url,text,comments
    都是str类型，通过re.split('\r',comments)分出每一条comment
'''
def deconstruct(path):
    news = open(path, 'rb')
    text = news.read()
    try:
        text = text.decode('utf8')
    except Exception:
        text = text.decode('utf8', 'ignore')
    news.close()
    text = re.subn('\n', '', text)
    types = ['source', 'title', 'time', 'url', 'text', 'comments']
    newText = {}
    for t in types:
        c = re.compile('<' + t + '>(.*?)</' + t + '>')
        temp = c.findall(text[0])
        if len(temp) == 0:
            print(path)
        else:
            newText[t] = temp[0]
    return newText