import os

ResourcePath = './ResourceSeg/'
SortedPath = './ResourceSorted/'

paths = [ResourcePath,SortedPath]
Num = [0,0]
for i in range(len(paths)):
    newsMedia = os.listdir(paths[i])
    for media in newsMedia:
        mediaPath = paths[i]+media+'/'
        months = os.listdir(mediaPath)
        for month in months:
            monthPath = mediaPath+month+'/'
            fileList = os.listdir(monthPath)
            Num[i] += len(fileList)

fw = open('./fileNum.txt','w',1,'utf8')
fw.write('Resource file Num:{0}\nSorted file Num:{1}'.format(Num[0],Num[1]))
fw.close()