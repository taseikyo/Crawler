#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-11 09:33:24
# @Author  : Lewis Tian (lewis.smith.tian@gmail.com)
# @Link    : https://github.com/LewisTian
# @Version : Python3.5

import requests
from bs4 import BeautifulSoup as BS
from urllib.request import urlretrieve
import sys
import os
from threading import Thread

s = requests.Session()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
}

def main(pid):
    url = 'https://tieba.baidu.com/p/'+pid+'?pn=1'
    r = s.get(url, headers = headers)
    bs = BS(r.text, 'html5lib')
    page = bs.find("li", {"class", "l_reply_num"}).findAll("span")[-1].text #页数
    data = bs.findAll("img", {"class", "BDE_Image"})
    Thread(target = download, args = (data, )).start()
    # download(data)

    if int(page) > 1:
        for i in range(2, int(page)+1):
            url = 'https://tieba.baidu.com/p/'+pid+'?pn='+str(i)
            r = s.get(url, headers = headers)
            bs = BS(r.text, 'html5lib')
            page = bs.find("li", {"class", "l_reply_num"}).findAll("span")[-1].text #页数
            data = bs.findAll("img", {"class", "BDE_Image"})
            Thread(target = download, args = (data, )).start()
            # download(data)            

def download(images):
    for x in images:
        print(x['src'])
        urlretrieve(x['src'], filename = sys.argv[1]+"/"+x['src'].split("/")[-1])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("[usage]: python image.py 2271504759")
    else:
        if not os.path.exists(sys.argv[1]):
            os.mkdir(sys.argv[1])
        main(sys.argv[1])
