#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-23 19:00:03
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import time
from random import choice
from calendar import monthrange
from threading import Thread
from concurrent import futures
import requests
import json
import pymysql

UA = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile ',
    'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
    'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
    'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+',
    'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
    'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) ',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
    'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999',
]

def info(date):
    start, end = date
    t = int(round(time.time() * 1000))
    data =  {
        'callback': '',
        'main_ver': 'v3',
        'search_type': 'video',
        'view_type': 'hot_rank',
        'order': 'click',
        'copy_right': '-1',
        'cate_id': '24',
        'page': '1',
        'pagesize': '20',
        'jsonp': 'jsonp',
        'time_from': date[0],
        'time_to': date[1],
        '_': t,
    }
    headers = {
        'Referer': 'https://www.bilibili.com/v/douga/mad/?spm_id_from=333.334.b_7072696d6172795f6d656e75.3',
        'User-Agent': choice(UA)
    }
    try:
        r = requests.get('https://s.search.bilibili.com/cate/search', params=data, headers=headers)
        print(r.json())
        with open(f'bili-mad/{date[0]}.json', 'w', encoding='utf-8') as f:
            json.dump(r.json(), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(date, e)

def dump(dates):
    data = []
    for x in dates:
        with open(f'bili-mad/{x[0]}.json', encoding='utf-8') as f:
            json_data = json.load(f)
        for d in json_data['result']:
            data.append(d['title'])
    with open('bili-mad.txt', 'w', encoding='utf-8') as f:
        f.write(' '.join(data))

def parse(dates):
    data = []
    for x in dates:
        with open(f'bili-mad/{x[0]}.json', encoding='utf-8') as f:
            json_data = json.load(f)
        for d in json_data['result']:
            data.append([d['id'], d['title'], d['author'], d['pic'], 
                        d['play'], d['favorites'], d['mid'], d['pubdate']])
    return data

def save2mysql(dates):
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', 
                               passwd='root', db='python')
        cursor = conn.cursor()
    except Exception as e:
        print(e)
        return
    data = parse(dates)
    sql = "insert into `bili-mad` values(%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        rows = cursor.executemany(sql, data)
        print(rows)
    except Exception as e:
        print(e)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    dates = []
    for y in range(2010, 2019):
        for m in range(1, 13):
            dates.append([f'{y}{m:02}01', f'{y}{m:02}{monthrange(y, m)[1]}'])
    with futures.ThreadPoolExecutor(32) as executor:
        executor.map(info, dates)
    save2mysql(dates)
