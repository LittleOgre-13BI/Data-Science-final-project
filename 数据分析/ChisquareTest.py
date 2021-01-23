import freqCount

'''
            |属于疫情报导|不属于疫情报导
包含某词     |A         |B
不包含某词   |C         |D
'''


def Chisquare(aimWord):
    A = float(freqCount.aimD(aimWord,1))
    B = float(freqCount.aimD(aimWord,-1))
    C = float(freqCount.totalD(1) - A)
    D = float(freqCount.totalD(-1) - B)

    result = (A+B+C+D)*(A*D-C*B)*(A*D-C*B)/(A+C)/(A+B)/(C+D)/(B+D)
    return result

if __name__ == '__main__':
    fw = open('./wordList.txt','rb')
    text = fw.read()
    try:
        text = text.decode('utf8')
    except Exception:
        text = text.decode('utf8', 'ignore')
    fw.close()
    wordList = text.split(',')
    data = {}
    for word in wordList:
        data[word] = Chisquare(word)

    wordslist = sorted(data.items(), key=lambda item:item[1], reverse=True)
    result = []
    for item in wordList:
        result.append('{0}:{1}\n'.format(item[0],item[1]))
    fw = open('./chisquareTestSque.txt','w',1,'utf8')
    fw.write(''.join(result))
    fw.close()

