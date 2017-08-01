#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-01 10:45:07
# @Author  : Lewis Tian (lewis.smith.tian@gmail.com)
# @Link    : https://github.com/LewisTian
# @Version : Python3.5

import requests
import re
import sys

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
}


def main(url):
    s = requests.Session()
    r = s.get(url, headers = headers)
    name = re.findall(r'cid=(\d+)&aid', r.text)[0]
    xml = 'https://comment.bilibili.com/'+name+'.xml'
    r = s.get(xml, headers = headers)
    data = re.findall(r'<d.*?>(.*?)</d>', r.text)
    with open(name+'.txt', 'w', encoding = 'utf-8') as f:
        for x in data:
            f.write(x+"\n")
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("input url...")
    else:
        main(sys.argv[1])
