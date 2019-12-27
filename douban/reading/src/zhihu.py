#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-19 15:00:08
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import re
import time
import requests
from random import randint
from glob import glob

DEDUPLIACATE = True

def main(pid='306249128'):
    # url = f'https://www.zhihu.com/api/v4/questions/306249128/answers'
    url = '' # 填入 url 再运行
    headers = {
        'x-requested-with': 'fetch',
        'referer': 'https://www.zhihu.com/question/306249128/answers/updated',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    payload = {
        'offset': '0',
        'limit': '20',
        'sort_by': 'updated',
    }
    is_end = False
    page = 1
    while not is_end:
        print(f'get page {page}...')
        # r = requests.get(url, headers=headers, params=payload)
        r = requests.get(url, headers=headers)
        # print(r.json())
        data = r.json()['data']
        is_end = r.json()['paging']['is_end']
        url = r.json()['paging']['next']
        
        answers = '\n'.join(x['excerpt'] for x in data)
        parse(answers, page)

        page += 1
        time.sleep(randint(500, 1000)/1000)

def parse(text, page):
    '''提取出所有 《书名》 格式的书名'''
    books = re.findall(r'《(.*?)》', text)
    if DEDUPLIACATE:
        books = set(books)
    with open(f'page-{page}.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(books))

def merge():
    books = []
    for x in glob("page-*.txt"):
        with open(x, encoding='utf-8') as f:
            data = f.readlines()
        books.extend([i.replace('\n', '') for i in data])
    if DEDUPLIACATE:
        books = set(books)
    with open('zhihu.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(books))

def calculate():
    books = {}
    for x in glob("page-*.txt"):
        with open(x, encoding='utf-8') as f:
            data = f.readlines()
        for i in data:
            i = i.replace('\n', '')
            if i in books:
                books[i] += 1
            else:
                books[i] = 1
    books = sorted(books.items(), key=lambda x: x[1], reverse=True)[:20]
    print(books)

if __name__ == '__main__':
    main()
    merge()
    calculate()