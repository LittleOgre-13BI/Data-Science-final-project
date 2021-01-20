import os
import re

path = './头条新闻/'

for mouth in range(1,7):
    chlidpath = path + '20200'+str(mouth)
    os.getcwd()
    fileList = os.listdir(chlidpath)
    for oldname in fileList:
        fw = open(chlidpath+'/'+oldname,'rb')
        text = fw.read()
        try:
            text = text.decode('utf8')
        except Exception:
            text = text.decode('utf8','ignore')
        fw.close()
        time = re.findall(r'<time>(.*?)</time>',text)
        time = re.findall(r'\d',time[0])
        time = ''.join(time)
        slic = re.sub('2020'+str(mouth),'',time)
        if len(slic) < 6:
            slic = '0'+slic
        time = '20200'+str(mouth)+slic
        os.rename(chlidpath+'/'+oldname,chlidpath+'/'+time+'.txt')