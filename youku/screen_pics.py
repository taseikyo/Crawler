#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-07 14:16:11
# @Author  : Lewis Tian (chasetichlewis@gmail.com)
# @GitHub  : https://github.com/LewisTian
# @Version : Python3.5

import requests
from bs4 import BeautifulSoup as BS
import re
import os

class Screeen(requests.Session):
    """docstring for Screeen"""
    def __init__(self, url):
        super(Screeen, self).__init__()
        self.url = url

    def __del__(self):
        self.close()

    def run(self):
        self.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
        })
        r = self.get(self.url)
        soup = BS(r.text, 'html5lib')
        ul = soup.find('ul', {'class', 'focus-list'})
        pics = ul.findAll('li')
        self.refine(pics[0]['style'])
        for x in pics[1:]:
            self.refine(x['_lazy'])
            

    def refine(self, tag):
        src = 'http:' + re.findall(r'url\((.*?)\)', tag)[0][1:-1]
        self.download(src)

    def download(self, src):
        if not os.path.exists('img'):
            os.mkdir('img')
        name = src.split('/')[-1] + '.jpg'
        r = self.get(src)
        with open('img/' + name, 'wb') as f:
            f.write(r.content)

if __name__ == '__main__':
    s = Screeen('http://www.youku.com/')
    s.run()


