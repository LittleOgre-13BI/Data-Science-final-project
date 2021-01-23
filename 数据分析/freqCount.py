import math
import re
import os
import textDeconstruct
import deconstruct

def wordList(path):
    wordList = []
    vectorsList = deconstruct.de()
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
                if word not in wordList:
                    wordList.append(word)
        else:
            newText = textDeconstruct.deconstruct(key)
            words = re.split('[|]', newText['text'])
            for word in words:
                if word not in wordList:
                    wordList.append(word)
    fw = open(path, 'w', 1, 'utf-8')
    fw.write(','.join(wordList))
    fw.close()



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

    wordslist = sorted(DF.items(), key=lambda item:item[1], reverse=True)
    return wordslist

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

def TFIDF(aimWord):
    TF = float(aimT(aimWord,0))/float(totalT(0))
    IDF = math.log(float(totalD(0))/float(aimD(aimWord,0)),10)

    return TF*IDF

if __name__ == '__main__':
    wordTF = {}
    fw = open('./wordList.txt','rb')
    text = fw.read()
    try:
        text = text.decode('utf8')
    except Exception:
        text = text.decode('utf8', 'ignore')
    fw.close()
    wordList = text.split(',')
    for word in wordList:
        wordTF[word] = aimT(word,0)

    wordslist = sorted(wordTF.items(), key=lambda item:item[1], reverse=True)
    result = []
    for item in wordList:
        result.append('{0}:{1}\n'.format(item[0],item[1]))
    fw = open('./wordsTF.txt','w',1,'utf8')
    fw.write(''.join(result))
    fw.close()