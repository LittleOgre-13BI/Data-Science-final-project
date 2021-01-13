from selenium import webdriver
import time,re,random
import userReader

browser = webdriver.Chrome(r".\chromedriver_win32\chromedriver.exe")
browser.get('http://weibo.com/')
time.sleep(30)
sumpage = 12147
fw = open("result1-12147.txt",'a')

def checkPages(d):
    try:
        element = d.find_element_by_class_name('W_pages')
    except Exception:
        return False
    return True

def checkNextpage(d):
    try:
        element = d.find_element_by_class_name('page next S_txt1 S_line1')
    except Exception:
        return ''

    return 'https://weibo.com'+re.findall(r'href="(.*?)"',element.text)[0]

def text(d):
    texts = d.find_elements_by_class_name('WB_detail')
    for text in texts:
        name = re.findall(r'【(.*?)】',text.text)
        if len(name) > 0:
            names = re.findall(r'[\u4e00-\u9fa5]',name[0])
            name = ''
            for word in names:
                name += word
            if len(name) > 0:
                print(name)
                if re.search(r'肺炎',name) is not None:
                    print('find the text')
                    global opt
                    try:
                        opt = text.find_element_by_class_name('WB_text_opt')
                    except Exception:
                        print('could find text opt url')

                    url = re.findall(r'href="(.*?)"',opt.text)
                    d.get('https:'+url)
                    time.sleep(30)

userList = userReader.users()

for user in userList:
    url = user['url']+'?is_all=1&stat_date=2019012#feedtop'

    # js = "document.documentElement.scrollBottom=200"
    # browser.execute_script(js)
    time.sleep(10)
    while url != '':
        browser.get(url)
        while not checkPages(browser):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(5)
        url = checkNextpage(browser)
        print('ready to select text')
        text(browser)


    # news = browser.find_elements_by_class_name('WB_detail')
    # for new in news:
    #     print(new.text)
    browser.close()
    break
