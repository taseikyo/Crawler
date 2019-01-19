#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-17 18:36:13
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

from selenium import webdriver
import requests
import threading
import re
import os
import time

"""
download bilibili logo images
"""

def download(html):
    banner = re.findall('class="head-logo".*?url\((.*?)\);">', html)
    if not banner: return
    name = banner[0].split('/')[-1].replace('&quot;','')
    if os.path.exists(f'images/{name}'): return
    link = banner[0].replace('&quot;','')
    r = requests.get(f'http:{link}')
    print(f'downloading {name}...')
    with open(f'images/{name}', 'wb') as f:
        f.write(r.content)


def browser(urls):
    '''发现除了首页logo直接在html中
    其他都是通过js生成的url，看不懂他怎么生成的
    本来代算直接都用requests请求，结果gg'''
    driver = webdriver.Chrome()
    driver.maximize_window()  # 最大化浏览器
    driver.implicitly_wait(8) # 设置隐式时间等待
    for url in urls:
        driver.get(url)
        threading.Thread(target=download, args=(driver.page_source, )).start()
        time.sleep(1.5)

if __name__ == '__main__':
    if not os.path.exists('images'):
        os.mkdir('images')
    x = ['https://www.bilibili.com/', 'https://www.bilibili.com/v/douga/', 'https://www.bilibili.com/anime/', 'https://www.bilibili.com/guochuang/',
        'https://www.bilibili.com/v/music/', 'https://www.bilibili.com/v/dance/', 'https://www.bilibili.com/v/game/', 'https://www.bilibili.com/v/technology/',
        'https://www.bilibili.com/v/digital/', 'https://www.bilibili.com/v/life/', 'https://www.bilibili.com/v/kichiku/', 'https://www.bilibili.com/v/fashion/',
        'https://www.bilibili.com/v/ad/ad/', 'https://www.bilibili.com/v/ent/', 'https://www.bilibili.com/v/cinephile/', 'https://www.bilibili.com/cinema/']
    browser(x)