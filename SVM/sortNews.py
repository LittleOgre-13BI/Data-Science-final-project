import os
import re
import svm
import textDeconstruct

'''
    对ResourceSeg里的新闻进行分类，将预测疫情相关报导的新闻输出到ResourceSorted目录下
'''

clf = svm.getSVMclf()
os.getcwd()
path = './ResourceSeg/'
newsMedia = os.listdir(path)
fw = open('./eigenWord.txt','rb')
text = fw.read()
fw.close()
text = text.decode('utf8','ignore')
eigenWord = text.split('\r\n')
fw = open('./weightVector.txt', 'rb')
text = fw.read()
text = text.decode('utf8', 'ignore')
fw.close()
text = text.split(',')
weight = [float(x) for x in text]
savePath = './ResourceSorted/'
if not os.path.exists(savePath):
    os.makedirs(savePath)
for media in newsMedia:
    mediaPath = path+media+'/'
    mediaSave = savePath+media+'/'
    months = os.listdir(mediaPath)
    if not os.path.exists(mediaSave):
        os.makedirs(mediaSave)
    for month in months:
        monthPath = mediaPath+month+'/'
        monthSave = mediaSave+month+'/'
        fileList = os.listdir(monthPath)
        if not os.path.exists(monthSave):
            os.makedirs(monthSave)
        for file in fileList:
            vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            filePath = monthPath+file
            fileSave = monthSave+file
            newText = {}
            text = ''
            if '人民日报' in media:
                fw = open(filePath,'rb')
                text = fw.read()
                fw.close()
                text = text.decode('utf8','ignore')
            else:
                newText = textDeconstruct.deconstruct(filePath)
                text = newText['text']

            words = re.split('[|]', text)
            for i in range(len(eigenWord)):
                if eigenWord[i] in words:
                    vector[i] = weight[i]
            y = clf.predict([vector])
            if y[0] == 1.0:
                fw = open(fileSave,'w',1,'utf8')
                if '人民日报' in media:
                    fw.write(text)
                else:
                    fw.write('<source>' + newText['source'] + '</source>' + '\n<title>' + newText[
                        'title'] + '</title>' + '\n<time>' +
                             newText['time'] + '</time>' + '\n<url>' + newText['url'] + '</url>' + '\n\n' + '\n<text>' +
                             newText[
                                 'text'] + '</text>' + '\n<comments>'
                             + '\n'.join(newText['comments']) + '</comments>')
                fw.close()
