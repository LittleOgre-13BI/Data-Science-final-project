import os
from selenium import webdriver
import time,re,random
import userReader
import text

browser = webdriver.Chrome(r".\chromedriver_win32\chromedriver.exe")
browser.get('http://weibo.com/')
aimRelevance = re.compile(r'肺炎|疫情|新冠|新型冠状|防疫|口罩|医疗物资|病毒')
time.sleep(30)


def checkPages(d):
    try:
        element = d.find_element_by_class_name('W_pages')
    except Exception:
        return False
    return True

def checkNextpage(d):
    try:
        element = d.find_element_by_class_name('W_pages')
        turnPage = element.find_elements_by_tag_name('a')
    except Exception:
        print("couldn't find next page url")
        return ''

    for item in turnPage:
        if item.get_attribute('class') == 'page next S_txt1 S_line1':
            return item.get_attribute('href')
    print("couldn't find next page url")
    return ''

def selectText(d):
    texts = d.find_elements_by_class_name('WB_detail')
    newsList = []
    for text in texts:
        state = False
        news = {}
        name = re.findall(r'【(.*?)】',text.text)
        name = ''.join(name)
        name = re.sub(r'<a(.*?)>#|#</a>', '', name)
        global topics
        try:
            topics = text.find_elements_by_class_name('a_topic')
        except Exception:
            print("couldn't find topics")

        for topic in topics:
            if aimRelevance.search(str(topic.text)) is not None:
                state = True


        if len(name) > 0 or state:
            if aimRelevance.search(name) is not None or state:
                news['title'] = name

                try:
                    opt = text.find_element_by_class_name('WB_text_opt')
                    news['url'] = str(opt.get_attribute('href'))
                    try:
                        source = text.find_element_by_class_name('WB_from')
                        source = source.find_elements_by_tag_name('a')
                        news['time'] = str(source[0].text)
                        news['source'] = str(source[1].text)
                        newsList.append(news)
                    except Exception:
                        # print("could't find text source")
                        pass
                except Exception:
                    # print(name+"couldn't find text opt url")
                    pass

    return newsList

def mkdir(path):

    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)

userList = userReader.users()

for user in userList:

    path = './'+user['name']
    mkdir(path)
    for month in range(1,7):
        childPath = path+'/20200'+str(7-month)
        mkdir(childPath)
        newsList = []
        url = user['url']+'?is_all=1&stat_date=20200'+str(7-month)

        while url != '':
            browser.get(url)
            time.sleep(5+random.randint(1,5))
            count = 0
            while not checkPages(browser):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                for _ in range(3):
                    time.sleep(1)
                    count+=1
                if count > 30:
                    break

            url = checkNextpage(browser)
            newsL = selectText(browser)
            for news in newsL:
                newsList.append(news)

        user['news'] = newsList
        text.getNewsDetail(browser,user['news'],childPath)
    # text.getNewsDetail(user['news'])

browser.close()

