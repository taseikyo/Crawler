#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-31 16:41:32
# @Author  : Lewis Tian (lewis.smith.tian@gmail.com)
# @Link    : https://github.com/LewisTian
# @Version : Python

import requests
import re

headers = {
    'Host':'cn.bing.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
}

def main():
    url = 'http://cn.bing.com'
    s = requests.Session()
    r = s.get(url, headers = headers)
    src = url + re.findall("g_img={url: \"(.*?)\"", r.text)[0]
    r = s.get(src, headers = headers)
    with open(src.split('/')[-1], 'wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    main()
