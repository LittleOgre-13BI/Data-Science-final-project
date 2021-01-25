import os
import re

'''
    检测训练集中打上的   标签      含义           标签值
                        <+>     疫情相关新闻       1
                        <->     非疫情相关新闻    -1
    生成文件的镜像分词文件路径与标签值的映射向量，存储文件result.txt
'''

path = 'C:/Users/86152/Desktop/大二上/数据科学/大作业/数据分析/训练集/'
os.getcwd()
list = os.listdir(path)
data = {}
for item in list:
    data[item] = []
    childPath = path+item+'/'
    fileList = os.listdir(childPath)
    for file in fileList:
        filePath = childPath+file
        fw = open(filePath,'rb')
        text = fw.read()
        try:
            text = text.decode('utf8')
        except Exception:
            text = text.decode('utf8', 'ignore')
        fw.close()
        vector = {}

        if re.search('<->',text) is not None:
            vector['./分词对照集/'+item+'/'+file] = -1
        else:
            vector['./分词对照集/'+item+'/'+file] = 1
        data[item].append(vector)


result = ''
for key in data.keys():
    result += key+':{\n'
    vstr = []
    for v in data[key]:
        for key in v.keys():
            vstr.append('({0},{1})'.format(key,v[key]))
    result += '\n'.join(vstr)+'}\n'
fw = open(path+'wordsDF.txt','w+',1,'utf8')
fw.write(result)
fw.close()

