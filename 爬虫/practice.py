import requests
from bs4 import BeautifulSoup

r = requests.get('https://search.sina.com.cn/?q=%E6%96%B0%E5%86%A0&range=title&c=news&sort=time')

r.raise_for_status()

soup = BeautifulSoup(r.text,"html.parser")
print(soup.find_all('span'))
