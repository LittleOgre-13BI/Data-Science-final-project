import re
import textDeconstruct

def proc(s):
    s = re.split('[|]', s)
    punctutation = " ＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､　、〃" \
                   "〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？#｡。!\"$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    for i in punctutation:
        for c in s:
            if i == c:
                s.remove(c)

    s = '|'.join(s)
    return s

filePath = r'C:\Users\86152\Desktop\202002031519.txt'
newText = textDeconstruct.deconstruct(filePath)
comments = newText['comments']
comments = re.split('\r', comments)
newComments = []
for comment in comments:
    if comment != '':
        comment = proc(comment)
        if comment != '':
            newComments.append(comment)

newText['comments'] = newComments

text = newText['text']
text = proc(text)
if text != '':
    newText['text'] = text
else:
    print('wrong text:'+filePath)

fw = open(filePath, 'w', 1, 'utf8')
fw.write('<source>' + newText['source'] + '</source>' + '\n<title>' + newText['title'] + '</title>' + '\n<time>' +
         newText['time'] + '</time>' + '\n<url>' + newText['url'] + '</url>' + '\n\n' + '\n<text>' + newText[
             'text'] + '</text>' + '\n<comments>'
         + '\n'.join(newText['comments']) + '</comments>')
fw.close()