import re


def de(path='./训练集/result.txt'):
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

if __name__ == '__main__':
    print(de())

