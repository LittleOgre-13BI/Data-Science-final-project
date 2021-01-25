import re


'''
    @:param path
    @:return newVectors--将向量映射关系以字典形式存储
    解析result.txt以python数据结构存储
'''
def de(path='./result.txt'):
    fw = open(path,'rb')
    text = fw.read()
    try:
        text = text.decode('utf8')
    except Exception:
        text = text.decode('utf8', 'ignore')
    fw.close()

    vectors = re.findall('\((.*?)\)',text)
    newVectors = {}
    for vector in vectors:
        vector = re.split(',',vector)
        newVectors[vector[0]] = int(vector[1])

    return newVectors

