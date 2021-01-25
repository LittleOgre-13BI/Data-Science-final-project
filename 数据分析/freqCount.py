import math
import re
import os
import textDeconstruct
import deconstruct

'''
    @:param path
    @:return
    统计训练集中的所有词，并以wordList.txt形式存储
'''
def wordList(path):
    wordList = []
    vectorsList = deconstruct.de()
    stopwords = [line.strip() for line in open('./stopwords_master/final_stopwords.txt', encoding='UTF-8').readlines()]
    for key in vectorsList.keys():
        if '人民日报训练集' in key:
            fw = open(key, 'rb')
            text = fw.read()
            try:
                text = text.decode('utf8')
            except Exception:
                text = text.decode('utf8', 'ignore')
            fw.close()
            words = re.split('[|]', text)
            for word in words:
                if word not in stopwords and  not word.isdigit() and '%' not in word and '.' not in word:
                    if word not in wordList and len(word) > 1:
                        wordList.append(word)
        else:
            newText = textDeconstruct.deconstruct(key)
            words = re.split('[|]', newText['text'])
            for word in words:
                if word not in stopwords and  not word.isdigit() and '%' not in word and '.' not in word:
                    if word not in wordList and len(word) > 1:
                        wordList.append(word)

    fw = open(path, 'w', 1, 'utf-8')
    fw.write('\n'.join(wordList))
    fw.close()

'''
    @:param
    @:return DF
    统计所有词的文档频率，并排序
'''
def DFcou():
    DF = {}
    path = './分词对照集/'
    os.getcwd()
    List = os.listdir(path)
    for item in List:
        childPath = path+item+'/'
        fileList = os.listdir(childPath)
        for file in fileList:
            if item == '人民日报训练集':
                fw = open(childPath + file, 'rb')
                text = fw.read()
                try:
                    text = text.decode('utf8')
                except Exception:
                    text = text.decode('utf8', 'ignore')
                fw.close()
                words = re.split('[|]',text)
                wordList = []
                for word in words:
                    if word not in wordList:
                        wordList.append(word)

                for word in wordList:
                    if word in DF:
                        DF[word] += 1
                    else:
                        DF[word] = 1
            else:
                newText = textDeconstruct.deconstruct(childPath+file)
                words = re.split('[|]', newText['text'])
                wordList = []
                for word in words:
                    if word not in wordList:
                        wordList.append(word)

                for word in wordList:
                    if word in DF:
                        DF[word] += 1
                    else:
                        DF[word] = 1
    DF = sorted(DF.items(), key=lambda item:item[1], reverse=True)
    return DF


'''
    @:param aimWord 目标词
            class_  type(class_)=int,类别：-1--非疫情报导
                                            1--疫情报导
                                            0--both
    @:return 目标词在某一类别的词频
'''
def aimT(aimWord,class_):
    num = 0
    vectorsList = deconstruct.de()
    for key in vectorsList.keys():
        if class_ == 0 or class_ == vectorsList[key]:
            if '人民日报' in key:
                fw = open(key, 'rb')
                text = fw.read()
                try:
                    text = text.decode('utf8')
                except Exception:
                    text = text.decode('utf8', 'ignore')
                fw.close()
                words = re.split('[|]', text)
                for word in words:
                    if word == aimWord:
                        num += 1
            else:
                newText = textDeconstruct.deconstruct(key)
                words = re.split('[|]', newText['text'])
                for word in words:
                    if word == aimWord:
                        num += 1
    return num


'''
    @:param aimWord 目标词
            class_  type(class_)=int,类别：-1--非疫情报导
                                            1--疫情报导
                                            0--both
    @:return 目标词在某一类别的文档频率
'''
def aimD(aimWord,class_):
    num = 0
    vectorsList = deconstruct.de()
    for key in vectorsList.keys():
        if class_ == 0 or class_ == vectorsList[key]:
            if '人民日报' in key:
                fw = open(key, 'rb')
                text = fw.read()
                try:
                    text = text.decode('utf8')
                except Exception:
                    text = text.decode('utf8', 'ignore')
                fw.close()
                words = re.split('[|]', text)
                for word in words:
                    if word == aimWord:
                        num += 1
                        break
            else:
                newText = textDeconstruct.deconstruct(key)
                words = re.split('[|]', newText['text'])
                for word in words:
                    if word == aimWord:
                        num += 1
                        break
    return num

'''
    @:param class_  type(class_)=int,类别：-1--非疫情报导
                                            1--疫情报导
                                            0--both
    @:return 某一类别的总文档频率
'''
def totalD(class_):
    num = 0
    vectorsList = deconstruct.de()
    if class_ == 0:
        num = len(vectorsList)
    else:
        for key in vectorsList.keys():
            if class_ == int(vectorsList[key]):
                num += 1
    return num

'''
    @:param class_  type(class_)=int,类别：-1--非疫情报导
                                            1--疫情报导
                                            0--both
    @:return 某一类别的总词率
'''
def totalT(class_):
    num = 0
    vectorsList = deconstruct.de()
    for key in vectorsList.keys():
        if class_ == 0 or class_ == vectorsList[key]:
            if '人民日报' in key:
                fw = open(key, 'rb')
                text = fw.read()
                try:
                    text = text.decode('utf8')
                except Exception:
                    text = text.decode('utf8', 'ignore')
                fw.close()
                words = re.split('[|]', text)
                num += len(words)
            else:
                newText = textDeconstruct.deconstruct(key)
                words = re.split('[|]', newText['text'])
                num += len(words)
    return num

'''
    @:param aimWord
    @:return tf-idf值
'''
def TFIDF(aimWord):
    TF = float(aimT(aimWord,0))/float(totalT(0))
    IDF = math.log(float(totalD(0))/float(aimD(aimWord,0)),10)
    return TF*IDF

'''
    @:param
    @:return
    通过遍历所有训练集中的新闻正文，查询特征词是否在该新闻中，以得到特征向量，并为其加权
    因为特征词共20个，加上label，向量共21维
    以文档路径--特征向量的方式存储在vectors.txt中
'''
def makeVectors():
    vectorsList = deconstruct.de()
    fw = open('./weightVector.txt','rb')
    text = fw.read()
    text = text.decode('utf8','ignore')
    fw.close()
    text = text.split(',')
    weight = [float(x) for x in text]
    fw = open('./eigenWord.txt','rb')
    text = fw.read()
    text = text.decode('utf8','ignore')
    fw.close()
    words = text.split('\r\n')
    result = []
    for key in vectorsList.keys():
        vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        vector[20] = float(vectorsList[key])
        if '人民日报' in key:
            fw = open(key, 'rb')
            text = fw.read()
            text = text.decode('utf8', 'ignore')
            fw.close()
        else:
            newText = textDeconstruct.deconstruct(key)
            text = newText['text']
        text = re.split('[|]', text)
        for i in range(len(words)):
            if words[i] in text:
                vector[i] = weight[i]
        vectorsList[key] = vector
        result.append('({0},{1})'.format(key, str(vector)))
    fw = open('vectors.txt', 'w', 1, 'utf8')
    fw.write('\n'.join(result))
    fw.close()


'''
    将vectors.txt解析，生成可供numpy加载的文件形式存储在SVM目录下
'''
if __name__ == '__main__':
    fw = open('vectors.txt', 'rb')
    text = fw.read()
    fw.close()
    text = text.decode('utf8','ignore')
    vectors = re.findall('\((.*?)\)',text)
    for i in range(len(vectors)):
        vector = vectors[i]
        vector = re.findall('\[(.*?)]',vector)
        vector = vector[0]
        vectors[i] = vector

    fw = open('../SVM/text.data','w',1,'utf8')
    fw.write('\n'.join(vectors))
    fw.close()
