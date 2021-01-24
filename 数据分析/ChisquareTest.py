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

    n = A+B+C+D
    temp = A*D-B*C
    # ea = (A+C)*(A+B)/n
    # eb = (A+B)*(B+D)/n
    # ec = (A+C)*(C+D)/n
    # ed = (C+D)*(B+D)/n
    # a = A-ea
    # b = B-eb
    # c = C-ec
    # d = D-ed
    # result = a*abs(a)/ea - b*abs(b)/eb - c*abs(c)/ec +d*abs(d)/ed

    result = n*temp*temp/(A+C)/(A+B)/(B+D)/(C+D)
    return result

if __name__ == '__main__':
    fw = open('./wordList2.txt','rb')
    text = fw.read()
    try:
        text = text.decode('utf8')
    except Exception:
        text = text.decode('utf8', 'ignore')
    fw.close()
    wordList = text.split('\r\n')
    l = len(wordList)
    num = 0
    proc = 0
    data = {}
    for word in wordList:
        data[word] = Chisquare(word)
        num += 1
        p = num * 100 / l
        if p > proc:
            print(p)
        proc = p

    wordslist = sorted(data.items(), key=lambda item:item[1], reverse=True)
    result = []
    for item in wordslist:
        result.append('{0}:{1}\n'.format(item[0],item[1]))
    fw = open('./chisquareTestSque.txt','w',1,'utf8')
    fw.write(''.join(result))
    fw.close()

