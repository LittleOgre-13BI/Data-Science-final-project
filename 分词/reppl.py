import re
import os
import textDeconstruct


'''
    @:param s--待处理的语料
    @:return s--处理后的语料
    将分词中后的语料中的中英文标点去掉
'''
def proc(s):
    s = re.split('[|]', s)
    punctutation = "＂＃＄ ％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､　、〃。…！" \
                   "〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？#｡。!\"$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    for i in punctutation:
        for c in s:
            if i == c:
                s.remove(c)
    s = '|'.join(s)
    return s


seg_path = "./ResourceSeg/"

cateList = os.listdir(seg_path)
for mydir in cateList:
    if mydir != '人民日报_seg' and mydir != '人民日报1_seg':
        continue
    seg_dir = seg_path+mydir+'/'
    dir_list = os.listdir(seg_dir)
    for dir_path in dir_list:
        segChild = seg_dir+dir_path+'/'
        childList = os.listdir(segChild)
        for file in childList:
            filePath = segChild+file
            if mydir == '人民日报_seg' or mydir == '人民日报1_seg':
                news = open(filePath, 'rb')
                text = news.read()
                try:
                    text = text.decode('utf8')
                except Exception:
                    text = text.decode('utf8', 'ignore')
                news.close()
                content = proc(text)
                if content == '':
                    print('wrong text:'+filePath)
                else:
                    fw = open(filePath,'w',1,'utf8')
                    fw.write(content)
                    fw.close()
            else:
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
                    print('wrong text:' + filePath)

                fw = open(filePath, 'w', 1, 'utf8')
                fw.write('<source>' + newText['source'] + '</source>' + '\n<title>' + newText[
                    'title'] + '</title>' + '\n<time>' +
                         newText['time'] + '</time>' + '\n<url>' + newText['url'] + '</url>' + '\n\n' + '\n<text>' +
                         newText[
                             'text'] + '</text>' + '\n<comments>'
                         + '\n'.join(newText['comments']) + '</comments>')
                fw.close()





