#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-20 22:19:27
# @Author  : Lewis Tian (chasetichlewis@gmail.com)
# @GitHub  : https://github.com/LewisTian
# @Version : Python3.5

import requests
from bs4 import BeautifulSoup as BS

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
}

def main():
    base_url = 'https://jandan.net/ooxx/page-{0}#comments'
    S = requests.Session()
    with open('picture.txt', 'w') as f:
        for x in range(1, 211):
            IMG = ""
            url = base_url.format(x)
            r = S.get(url, headers = headers)
            bs = BS(r.text, 'html5lib')
            pic_list = bs.find('ol', {'class', 'commentlist'}).findAll('li') # picture list
            for i in pic_list:
                try:
                    raw_pic = 'http:' + i.find('a', {'class', 'view_img_link'})['href'] # raw image link
                    IMG += raw_pic + '\n'
                except:
                    pass
            f.write(IMG)
            f.flush()

if __name__ == '__main__':
    main()