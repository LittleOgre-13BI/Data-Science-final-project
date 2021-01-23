import os
from selenium import webdriver
import time,re,random
import userReader
import text

#TODO 这是需要用的工具selenium的webdriver，你装好了后下面输打开这个程序的path
browser = webdriver.Chrome(r".\chromedriver_win32\chromedriver.exe")

browser.get('http://weibo.com/')
aimRelevance = re.compile(r'肺炎|疫情|新冠|新型冠状|防疫|口罩|医疗物资|病毒|病例')
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

def checkTime(src,dest):
    for i in range(0, 3):
        a = int(dest[i * 2 : i * 2 + 2])
        b = int(src[i * 2 : i * 2 + 2])
        if a > b:
             return True
    return False


def selectText(d,processTime):
    texts = d.find_elements_by_class_name('WB_detail')
    newsList = []
    for text in texts:
        state = False
        news = {}
        name = re.findall(r'【(.*?)】',text.text)
        name = ''.join(name)
        name = re.sub(r'<a(.*?)>#|#</a>', '', name)
        if name is None or name == '':
            name =text.text
            news['title'] = ''
        else:
            news['title'] = name

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
                try:
                    opt = text.find_element_by_class_name('WB_text_opt')
                    news['url'] = str(opt.get_attribute('href'))
                    try:
                        source = text.find_element_by_class_name('WB_from')
                        source = source.find_elements_by_tag_name('a')
                        news['time'] = str(source[0].text)
                        t = re.split(r'\D', news['time'])
                        for i in range(1, 3):
                            if len(t[i]) < 2:
                                t[i] = '0' + t[i]
                        t = ''.join(t)
                        if checkTime(processTime,t[6:]):
                            continue
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

def checkProcess(p):
    os.getcwd()
    fileList = os.listdir(p)
    aimTime = p[-6:]
    processTime = '312359'
    if len(fileList) > 0:
        file = fileList[0]
        file = file[:-4]
        time = re.sub(aimTime, '', file)
        if len(time) < 6:
            time = '0'+time
        processTime = time
    return processTime

#TODO userList是列表形式装你要采集的用户的名字和网址，用户以字典的形式,你需要改一下
#例:userList = [{'name':'中国新闻网','url':'https://weibo.com/chinanewsv'}]
userList = userReader.users()

for user in userList:

    path = './'+user['name']
    mkdir(path)
    for month in range(1,8):

        if month == 7:
            aimTime = '201912'
        else:
            aimTime = '20200'+str(7-month)

        childPath = path+'/'+aimTime
        mkdir(childPath)
        pTime = checkProcess(childPath)
        if pTime[0:1] == '01':
            continue

        newsList = []
        url = user['url']+'?is_all=1&stat_date=20200'+str(7-month)
        times = 6

        while url != '':
            browser.get(url)
            time.sleep(5+random.randint(1,5))
            count = 0
            state = False
            while not state:
                state = checkPages(browser)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                for _ in range(3):
                    time.sleep(1)
                    count+=1
                if count > 30:
                    break

            if not state or (times == 0):
                times-=1
                continue

            url = checkNextpage(browser)
            newsL = selectText(browser,pTime)
            for news in newsL:
                newsList.append(news)

        user['news'] = newsList
        text.getNewsDetail(browser,user['news'],childPath)
    # text.getNewsDetail(user['news'])

browser.close()

