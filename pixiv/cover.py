#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-19 15:10:14
# @Author  : Lewis Tian (lewis.smith.tian@gmail.com)
# @Link    : https://github.com/LewisTian
# @Version : Python3.5

import requests
from bs4 import BeautifulSoup as BS
import json
import re

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
}

def main():
    url = 'https://www.pixiv.net/'
    session = requests.Session()
    r = session.get(url, headers = headers)
    json_data = BS(r.text, 'html5lib').find('input', {'class', 'json-data'})['value']
    # 'https://i.pximg.net/img-master/img/'
    data = json.loads(json_data)['pixivBackgroundSlideshow.illusts']['landscape']
    for x in data:
        referer = x['www_member_illust_medium_url']
        m = x['url']['medium']
        l = x['url']['1200x1200']
        name = re.findall(r'(\d+\_.*)', l)[0]
        print(name)
        # print(referer, m, l)
        headers['referer'] = referer
        r = session.get(l, headers = headers)
        with open(name, 'wb') as f:
            f.write(r.content)

if __name__ == '__main__':
    main()
