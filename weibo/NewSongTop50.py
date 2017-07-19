#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-19 20:34:02
# @Author  : Lewis Tian (lewis.smith.tian@gmail.com)
# @Link    : https://github.com/LewisTian
# @Version : python3.5

import requests
import time
from openpyxl import Workbook

wb = Workbook()
filename = ''
ws1 = wb.active
ws1.title = "微博亚洲新歌榜"
ws1['A1'] = "歌名"
ws1['B1'] = "歌手"
ws1['C1'] = "排名"
ws1['D1'] = "分数"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
}

def main(date):
    url = 'http://pop.weibo.com/ajax_getdata'
    name = []  
    singer = []  
    rank = []  
    score = []
    data = {
        'type':'trend',
        'date':date
    }
    r = requests.post(url, data = data,headers = headers)
    rank_list = r.json()['list']['data']
    for x in rank_list:
        name.append(x['songname'])
        for k,v in x['singers'].items():
            singer.append(v)
        rank.append(x['rank'])
        score.append(x['score'])

    for (i, m, o, p) in zip(name, singer, rank, score):
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
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    filename = '微博亚洲新歌榜_'+date+'.xlsx'
    main(date)
