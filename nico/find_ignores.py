# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

ptn = re.compile('(.+)（(.+)）')

res = requests.get('https://dic.nicovideo.jp/a/%E8%AA%AD%E3%81%BF%E3%81%8C%E9%80%9A%E5%B8%B8%E3%81%AE%E8%AA%AD%E3%81%BF%E6%96%B9%E3%81%A8%E3%81%AF%E7%95%B0%E3%81%AA%E3%82%8B%E8%A8%98%E4%BA%8B%E3%81%AE%E4%B8%80%E8%A6%A7')

soup = BeautifulSoup(res.text, 'lxml')
for li in soup.find_all('li'):
    text = li.get_text()
    match = ptn.fullmatch(text)
    if match:
        print(match.group(1))
