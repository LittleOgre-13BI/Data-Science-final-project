import os
import textDeconstruct
# 写入文件
def savefile(savepath, content):
    with open(savepath, "a+", encoding="utf-8") as f:
        f.write(content)

# 读取文件
def readfile(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return content

# 清除文本
def cleanfile(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write('')

# 以字典形式构建情感词典 key是情感词，value是权重
def getSenDic():
    with open(".\\Dictionary\\dictionary.txt", "r", encoding="utf-8") as f:
        temp = f.readlines()
    sen_dic = dict()
    for s in temp:
        if (s.split('\t')[3] == '2\n'):
            sen_dic[s.split('\t')[0]] = ((int)(s.split('\t')[2])) * -1
        if (s.split('\t')[3] == '1\n'):
            sen_dic[s.split('\t')[0]] = (int)(s.split('\t')[2])
    return sen_dic

# 以list形式构建否定词典
def getNotList():
    with open(".\\Dictionary\\not.txt", "r") as f:
        not_list  = f.readlines()
    for i in range(len(not_list)):
        not_list[i] = not_list[i].split('\n')[0]
    return not_list

# 构建程度词典
def getDegreeDic():
    with open(".\\Dictionary\\degree.txt", "r") as f:
         temp  = f.readlines()
    degree_dic = dict()
    for s in temp:
        temp2 = s.split('\n')[0]
        degree_dic[temp2.split(',')[0]] = float(temp2.split(',')[1])
    return degree_dic

# 读取文件内容
def calculate():
    # 构建字典
    sen_dic = getSenDic()
    not_list = getNotList()
    degree_dic = getDegreeDic()

    cleanfile("resourceAnalysed.txt")
    rootdir = '.\\ResourceSorted'
    list = os.listdir(rootdir)
    temp = []
    for i in range(0,len(list)):
        temp.append(os.path.join(rootdir,list[i]))
    for i in temp:
        list = os.listdir(i)
        for j in range(len(list)):
            corpus_path = os.path.join(i,list[j])
            catelist = os.listdir(corpus_path)
            for mydir in catelist:
                class_path = corpus_path  + "\\"+ mydir
                content = textDeconstruct.deconstruct(class_path)['text'].split('|')

            # 计算情绪权值
                result = 0
                for m in range(1,len(content)):
                    if content[m] in sen_dic.keys():
                        if content[m-1] in not_list:
                            result += (sen_dic[content[m]] * -1)
                        elif content[m-1] in degree_dic.keys():
                            result += (sen_dic[content[m]] * (degree_dic[content[m-1]]))
                        else:
                            result += sen_dic[content[m]]
                result = str(result)
                savefile("resourceAnalysed.txt",'('+class_path + ',' + result + ')' + '\n')

if __name__ == '__main__':
    calculate()
    print('finished')
