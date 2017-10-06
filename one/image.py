#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-06 16:09:35
# @Author  : Lewis Tian (chasetichlewis@gmail.com)
# @GitHub  : https://github.com/LewisTian
# @Version : Python3.5

import requests
from bs4 import BeautifulSoup as BS

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
}

def main():
    url = 'http://www.wufazhuce.com/'
    s = requests.Session()
    r = s.get(url, headers = headers)    
    bsObj = BS(r.text, 'html5lib')
    imgs = bsObj.find_all('img', {'class', 'fp-one-imagen'})
    for x in imgs:
        name = x['src'].split('/')[-1] + '.jpeg'
        r = s.get(x['src'], headers = headers)
        with open(name, 'wb') as f:
            f.write(r.content)


if __name__ == '__main__':
    main()


