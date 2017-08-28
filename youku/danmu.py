#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-25 10:04:41
# @Author  : Lewis Tian (chasetichlewis@gmail.com)
# @Link    : https://github.com/LewisTian
# @Version : Python3.5

import requests
import time

s = requests.Session()

headers = {
    'Referer':'http://v.youku.com/v_show/id_XNTQwMTgxMTE2.html',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
}

data = {
    'iid':'135045279',
    'begin':'0',
    'type':'1',
    'ct':'1001',
    'cid':'100',
    'ouid':'135922191',
    'lid':'0',
    'aid':'19461',
}

def Danmu(data):
    for x in data:
        print(x['content'])

def main():
    url = "http://service.danmu.youku.com/pool"
    r = requests.post(url, headers = headers, data = data)
    json = r.json()
    count = json['count']
    current = json['current']
    danmu = json['data']
    _next = json['next']
    Danmu(danmu)
    for x in range(1, count):
        time.sleep(5)
        data['begin'] = x
        r = requests.post(url, headers = headers, data = data)
        json = r.json()
        danmu = json['data']
        Danmu(danmu)

if __name__ == '__main__':
    main()
