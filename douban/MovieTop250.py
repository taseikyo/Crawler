#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-17 20:10:14
# @Author  : Lewis Tian (lewis.smith.tian@gmail.com)
# @Link    : https://github.com/LewisTian
# @Version : Python3.5

__author__ = 'Lewis Tian'

import requests
import re
from bs4 import BeautifulSoup as BS
from openpyxl import Workbook

wb = Workbook()
filename = '电影.xlsx'
ws1 = wb.active
ws1.title = "电影top250"
ws1['A1'] = "电影名"
ws1['B1'] = "评价人数"
ws1['C1'] = "评分"
ws1['D1'] = "短评"



headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
}

def main():
    url = 'https://movie.douban.com/top250'
    name = []  
    star_num = []  
    score = []  
    quote = []
    i = 1
    download_url = url
    while i <= 10:
        r = requests.get(download_url, headers = headers)
        data = BS(r.text, 'html5lib').find('ol', {'class', 'grid_view'}).findAll('li')
        for x in data:
            item = x.find('div', {'class', 'info'})
            name.append(item.find('span',{'class','title'}).text)
            score.append(item.find('span',{'class','rating_num'}).text)
            num = item.find('div',{'class','star'}).findAll('span')[-1].text
            star_num.append(re.findall(r'(\d+)', num)[0])
            if item.find('span',{'class','inq'}):
                quote.append(item.find('span',{'class','inq'}).text)
            else:
                quote.append(" ")
        download_url = url + '?start='+str(25*i)+'&filter='
        i = i + 1
    for (i, m, o, p) in zip(name, star_num, score, quote):
        col_A = 'A%s' % (name.index(i) + 2)
        col_B = 'B%s' % (name.index(i) + 2)
        col_C = 'C%s' % (name.index(i) + 2)
        col_D = 'D%s' % (name.index(i) + 2)
        ws1[col_A] = i
        ws1[col_B] = m
        ws1[col_C] = o
        ws1[col_D] = p
    wb.save(filename = filename)

if __name__ == '__main__':
    main()
