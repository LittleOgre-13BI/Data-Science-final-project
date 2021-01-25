import requests  # 发送网络请求，接收服务器返回的数据
import bs4  # 解析html内容
import os  # 将数据输入存储到本地文件中
import datetime


def fetchUrl(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.116 Safari/537.36 '
    }

    r = requests.get(url, headers)
    r.raise_for_status()  # 判断访问是否成功
    r.encoding = r.apparent_encoding
    return r.text  # 网页的html内容


def getPageList(year, month, day):
    url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/nbs.D110000renmrb_01.htm'
    html = fetchUrl(url)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    # pageList=bsobj.find('div', attrs= {'id': 'pageList'}).ul.find_all('div', attrs = {'class': 'right_title_name'})
    temp = bsobj.find('div', attrs={'id': 'pageList'})
    if temp:
        pageList = temp.ul.find_all('div', attrs={'class': 'right_title-name'})
    else:
        pageList = bsobj.find('div', attrs={'class': 'swiper-container'}).find_all('div',
                                                                                   attrs={'class': 'swiper-slide'})
    linkList = []
    for page in pageList:
        link = page.a["href"]
        url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
        linkList.append(url)
    return linkList


def getTitleList(year, month, day, pageUrl):
    '''
    :param year:
    :param month:
    :param day:
    :param pageUrl: 版面链接
    :return: 报纸某一版面的文章链接列表
    '''
    html = fetchUrl(pageUrl)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    # titleList=bsobj.find('div', attrs={'id': 'titleList'}).ul.find_all('li')
    temp = bsobj.find('div', attrs={'id': 'titleList'})
    if temp:
        titleList = temp.ul.find_all('li')
    else:
        titleList = bsobj.find('ul', attrs={'class': 'news-list'}).find_all('li')
    linkList = []
    for title in titleList:
        tempList = title.find_all('a')
        for temp in tempList:
            link = temp["href"]
            if 'nw.D110000renmrb' in link:
                url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
                linkList.append(url)
    return linkList


def getContent(html):
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    title = bsobj.h3.text + '\n' + bsobj.h1.text + '\n' + bsobj.h2.text + '\n'
    print(title)
    pList = bsobj.find('div', attrs={'id': 'ozoom'}).find_all('p')
    content = ''
    for p in pList:
        content += p.text + '\n'
    print(content)
    resp = title + content
    return resp


def saveFile(content, path, filename):
    if not os.path.exists(path):
        os.makedirs(path)  # 如果没有该文件夹则自动生成
    with open(path + filename, 'w', encoding='utf-8') as f:
        f.write(content)


def download_rmrb(year, month, day, destdir):
    pageList = getPageList(year, month, day)
    for page in pageList:
        titleList = getTitleList(year, month, day, page)
        for url in titleList:
            # 获取新闻文章内容
            html = fetchUrl(url)
            content = getContent(html)

            # 生成保存的文件路径及文件名
            temp = url.split('_')[2].split('.')[0].split('-')
            pageNo = temp[1]
            titleNo = temp[0] if int(temp[0]) >= 10 else '0' + temp[0]
            path = destdir + '/' + year + month + day + '/'
            fileName = year + month + day + '-' + pageNo + '-' + titleNo + '.txt'

            # 保存文件
            saveFile(content, path, fileName)


def gen_dates(b_date, days):
    day = datetime.timedelta(days=1)
    for i in range(days):
        yield b_date + day * i


def get_date_list(beginDate, endDate):
    """
    获取日期列表
    :param start: 开始日期
    :param end: 结束日期
    :return: 开始日期和结束日期之间的日期列表
    """

    start = datetime.datetime.strptime(beginDate, "%Y%m%d")
    end = datetime.datetime.strptime(endDate, "%Y%m%d")

    data = []
    for d in gen_dates(start, (end - start).days):
        data.append(d)

    return data


if __name__ == '__main__':
    '''
    newsDate = input("请输入日期（格式如20200101）：")
    year = newsDate[0:4]
    month = newsDate[4:6]
    day = newsDate[6:8]
    destdir = "D:/data"
    download_rmrb(year, month, day, destdir)
    print("done:"+year+month+day)
    '''
    beginDate = input('请输入开始日期:')
    endDate = input('请输入结束日期:')
    data = get_date_list(beginDate, endDate)

    for d in data:
        year = str(d.year)
        month = str(d.month) if d.month >= 10 else '0' + str(d.month)
        day = str(d.day) if d.day >= 10 else '0' + str(d.day)
        download_rmrb(year, month, day, 'D:/data')
        print("done")

