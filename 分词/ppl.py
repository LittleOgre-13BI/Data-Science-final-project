import re
import jieba
import os
import reppl

def savefile(savepath, content):
    fp = open(savepath, "wb")
    fp.write(content)
    fp.close()


def readfile(path):
    fp = open(path, "rb")
    content = fp.read()
    fp.close()
    return content

seg_path = "./ResourceSeg/"
corpus_path = "./Resource/"
os.getcwd()
catelist = os.listdir(corpus_path)
for mydir in catelist:

    # if mydir == '人民日报' or mydir == '人民日报1':
    #     continue

    class_path = corpus_path + mydir + "/"
    seg_dir = seg_path + mydir + "_seg/"
    if not os.path.exists(seg_dir):
        os.makedirs(seg_dir)
    # 获取类别目录下的所有目录

    dir_list = os.listdir(class_path)
    # 将类别下面的所有目录遍历出来
    for dir_path in dir_list:
        dirpath = class_path + dir_path + "/"
        segChild = seg_dir + dir_path + "/"
        if not os.path.exists(segChild):
            os.makedirs(segChild)

        childList = os.listdir(dirpath)
        for file in childList:
            # 拼出文件名全路径
            fullname = dirpath + file
            # 读取文件内容

            if mydir == '人民日报' or mydir == '人民日报1':
                content = readfile(fullname).strip()
                # 将换行替换掉
                content = content.replace('\r\n'.encode(), ''.encode()).strip()
                # 为文件内容分词
                content_seg = jieba.cut(content)
                # 将处理后的文件保存到分词后的语料目录
                savefile(segChild + file, "|".join(content_seg).encode())
            else:
                news = open(fullname,'rb')
                text = news.read()
                try:
                    text = text.decode('utf8')
                except Exception:
                    text = text.decode('utf8', 'ignore')
                news.close()
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

                text = newText['text']
                text = re.subn('\r','',text)
                text_seg = jieba.cut(text[0])
                newText['text'] = reppl.proc('|'.join(text_seg))

                comments = newText['comments']
                comments = re.split('\r',comments)
                for i in range(len(comments)):
                    comment_seg = jieba.cut(comments[i])
                    comments[i] = reppl.proc('|'.join(comment_seg))

                newText['comments'] = comments
                fw = open(segChild + file, 'w+',1,'utf8')
                fw.write('<source>' + newText['source'] + '</source>' + '\n<title>' + newText['title'] + '</title>' + '\n<time>' +
                     newText['time'] + '</time>' + '\n<url>' + newText['url'] + '</url>' + '\n\n' + '\n<text>' + newText[
                         'text'] + '</text>' + '\n<comments>'
                     + '\n'.join(newText['comments']) + '</comments>')
                fw.close()


