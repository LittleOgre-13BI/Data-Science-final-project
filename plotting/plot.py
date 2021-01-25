from matplotlib import ticker
from matplotlib import pyplot as plt
import dataProcessing
import numpy as np
import time

'''
    将各媒体各时间段的大众心态值散点通过最小二乘法回归拟合成曲线，并可视化
'''

vectors = dataProcessing.data()
fig, ax = plt.subplots()
tick_spacing = 5
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
plt.xticks(fontsize=8)
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
ax.axhline(0,color='black')
for media in vectors.keys():
    ts = []
    y = []
    for key in vectors[media].keys():
        ts.append(key)
        y.append(vectors[media][key])

    t = [time.mktime(time.strptime(d,'%Y%m%d')) for d in ts]
    t = np.array(t)
    power = 4
    parameter = np.polyfit(t,y,power)
    y2 = np.zeros(len(t))
    for i in range(power+1):
        y2 += parameter[i] * t ** (power-i)
    t2 = [time.strftime('%Y-%m-%d',time.localtime(d)) for d in t]
    ax.set_xlabel('时间')
    ax.set_ylabel('心态值')
    ax.plot(t2,y2,label=media)
    # 散点图
    # ax.scatter(t2,y)

ax.legend()
plt.show()
