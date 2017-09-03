#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-03 20:20:38
# @Author  : Lewis Tian (chasetichlewis@gmail.com)
# @GitHub  : https://github.com/LewisTian
# @Version : Python3.5

import requests
from bs4 import BeautifulSoup as BS
import time
import os
import json

headers = {
    'Cookie':{Cookie},
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
}

s = requests.Session()

def main(url):
    r = s.get(url, headers = headers)
    data = r.json()['data']
    for x in data:
        getUrl(x['content'])
        # print(x['content'])

def getUrl(card):
    # print(card)
    card = BS(card, "html5lib")
    images = card.findAll("img")
    for i in images:
        try:
            url = i['data-original']
            print(url)
        except Exception as e:
            url = i['src']
            print(url)
        download(url)
        time.sleep(3)

def download(url):
    r = s.get(url, headers = headers)
    name = url.split("/")[-1]
    if not os.path.exists(name):
        with open(name, "wb") as f:
            f.write(r.content)

if __name__ == '__main__':
    #有哪些比女主更招人喜欢的女二？
    include = "include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"
    offset = "offset=0" #起始位置
    limit = "limit=20" #请求数
    sort_by = "sort_by=default"
    main("https://www.zhihu.com/api/v4/questions/64629919/answers?"+include+"&"+offset+"&"+limit+"&"+sort_by)
