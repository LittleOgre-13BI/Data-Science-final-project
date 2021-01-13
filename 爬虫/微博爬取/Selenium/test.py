import re

s = '【“<a target="_blank" render="ext" suda-uatrack="key=topic_click&amp;value=click_topic" class="a_topic" extra-data="type=topic" href="//s.weibo.com/weibo?q=%23%E6%AD%A6%E6%B1%89%E4%BB%81%E7%88%B1%E5%8C%BB%E9%99%A2%E6%B3%95%E4%BA%BA%E4%BB%A3%E8%A1%A8%E4%B8%BA%E8%80%81%E8%B5%96%23&amp;from=default">#武汉仁爱医院法人代表为老赖#</a>” 院长：我们是莆系但不坏】'

name = re.findall(r'【(.*?)】',s)

name = ''.join(name)
name = re.sub(r'<a(.*?)>#|#</a>','',name)
print(name)