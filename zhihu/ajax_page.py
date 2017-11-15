#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-15 19:55:18
# @Author  : Lewis Tian (chasetichlewis@gmail.com)
# @GitHub  : https://github.com/LewisTian
# @Version : Python3.5
'''
爬取知乎第二页及其之后页面数据
'''
import requests
import re

base = 'https://www.zhihu.com/'

headers = {
    'Cookie':$cookie,
    'Host':'www.zhihu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
}

S = requests.Session()

def main():
    r = S.get(base, headers = headers)
    # 首页数据我未做提取处理
    raw = r.text.replace('&quot;', '"').replace('&amp;', '&')
    xUDID = re.findall(r'"xUDID":"(.*?)"', raw)[0]
    authorization = re.findall(r'"carCompose":"(.*?)"', raw)[0]
    next_ajax = re.findall(r'"next":"(.*?)"', raw)[0]
    headers['X-API-VERSION'] = '3.0.53'
    headers['X-UDID'] = xUDID
    headers['authorization'] = 'Bearer ' + authorization
    while next_ajax:
        r = S.get(next_ajax, headers = headers)
        data = r.json()['data']
        next_ajax = r.json()['paging']['next']
        parse(data)

def parse(data):
    """解析数据 此处我仅提取的答主id"""
    for x in data:
        author = x['target']['author']['name']
        print(author)

if __name__ == '__main__':
    main()



