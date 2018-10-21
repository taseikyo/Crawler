#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-21 19:33:57
# @Author  : Lewis Tian (chtian@hust.edu.cn | 2471740600@qq.com)
# @Link    : https://lewistian.github.io/
# @Version : Python3
# @Description : get cover according to the av num

import requests
import sys
import re

def main(av):
    url = 'https://www.bilibili.com/video/av' + av
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
    }
    r = requests.get(url, headers = headers)
    src = re.findall(r'<meta data-vue-meta="true" itemprop="image" content="(.*?)"/>', r.text)[0]
    print(src) # cover link

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'[usage] python {__file__} av2333')
    else:
        main(re.findall(r'av(\d+)', sys.argv[1])[0])
