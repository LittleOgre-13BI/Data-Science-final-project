import re


'''
    @:param
    @:return d--d={media1:{time1:data1,...},...}
    解析resourceAnalysed.txt得到各媒体各时段的大众心态值
'''
def data():
    fw = open('./resourceAnalysed.txt','rb')
    text = fw.read()
    fw.close()
    text = text.decode('utf8','ignore')

    vectors = re.findall('\((.*?)\)',text)
    vectorList = {}
    for vector in vectors:
        path,value = vector.split(',')
        mediaName = re.findall(r'ed\\(.*?)_seg',path)[0]
        if mediaName not in vectorList.keys():
            vectorList[mediaName] = {}
        if abs(float(value)) > 100:
            continue
        time = re.findall(r'\d\\(.*?)\.txt',path)[0]
        if '201912' in time:
            continue
        vectorList[mediaName][time] = float(value)


    newVectors = {}
    for media in vectorList.keys():
        if media not in newVectors.keys():
            newVectors[media] = {}
        for key in vectorList[media]:
            time = key[0:8]
            if time not in newVectors[media].keys():
                newVectors[media][time] = [vectorList[media][key],]
            else:
                newVectors[media][time].append(vectorList[media][key])

    date = []
    for media in newVectors.keys():
        if len(date) == 0:
            date = newVectors[media].keys()
        else:
            date = list(set(date) & set(newVectors[media].keys()))

    d = {}
    for media in newVectors.keys():
        if media not in d.keys():
            d[media] = {}
        for key in newVectors[media].keys():
            if key not in date:
                continue
            total = 0
            l = len(newVectors[media][key])
            for item in newVectors[media][key]:
                total += item
            average = total/l
            d[media][key] = average
    return d

if __name__ == '__main__':
    print(data())