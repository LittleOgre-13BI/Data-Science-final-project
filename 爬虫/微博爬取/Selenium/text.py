import random
import time
import re
from selenium import webdriver

def checkBottom(d):
    try:
        element = d.find_element_by_class_name('more_txt')
    except Exception:
        return False
    return True

def getNewsDetail(d,newsList,path):

    for news in newsList :
        d.get(news['url'])
        time.sleep(5 + random.randint(1, 5))
        try:
            t = d.find_element_by_class_name('WB_detail')
            news['text'] = re.sub(r'k收起\nf查看大图\nm向左旋转\nn向右旋转','',t.text)
        except Exception:
            news['text'] = "couldn't find the text"
        count = 0
        while not checkBottom(d):
            d.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            for _ in range(3):
                time.sleep(1)
                count += 1
            if count > 15:
                break
        commentList = []
        try:
            comments = d.find_element_by_class_name('list_ul')
            comments = comments.find_elements_by_tag_name('div')
            for comment in comments:
                if comment.get_attribute('node-type') is not None:
                    if comment.get_attribute('node-type') == 'root_comment':
                        commentText = comment.find_element_by_class_name('WB_text')
                        commentList.append(commentText.text)
                if len(commentList) == 30:
                    break
        except Exception:
            pass
        
        news['comments'] = commentList
        t = re.split(r'\D', news['time'])
        for i in range(1,3):
            if len(t[i]) < 2:
                t[i] = '0'+t[i]
        t = ''.join(t)
        fw = open(path + '/' + t + '.txt', 'w', encoding='utf-8')
        fw.write('<source>' + news['source'] + '</source>' + '\n<title>' + news['title'] + '</title>' + '\n<time>' +
                 news['time'] + '</time>' + '\n<url>' + news['url'] + '</url>' + '\n\n' + '\n<text>' + news[
                     'text'] + '</text>' + '\n<comments>'
                 + '\n'.join(news['comments']) + '</comments>')

def exec():
    browser = webdriver.Chrome(r".\chromedriver_win32\chromedriver.exe")
    browser.get('http://weibo.com/')
    time.sleep(30)
    newsDetail = getNewsDetail(browser,[{'url':'https://weibo.com/2028810631/J7aL3nuYl?type=comment#_rnd1610408889653'}])
    fw = open('1.text','w')
    for news in newsDetail:
        fw.write(news['text']+'\n')
        fw.write('\ncomment:\n')
        for comment in news['comments'] :
            fw.write(comment+"\n")
    fw.close()

if __name__ == '__main__':
    exec()
