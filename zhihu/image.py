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
    'Cookie':'q_c1=11022fc20ce84bdfa6ae41885ca7729c|1504012419000|1504012419000; q_c1=1a46edc07bcf4a008c0c855352445266|1504012420000|1504012420000; _zap=6bc79ae7-e55b-41cf-826d-9be8a7728d57; r_cap_id="N2U5ODhlMDY1ZDE4NDUyZmE1N2JlY2ViMzMyNmI0Mjk=|1504070278|2904048bf1f29d83be4798145d78505866a11e68"; cap_id="NTQ0OGQ4NzM2ZmYyNDQ2NmIxNjk4NmM5ZjUyOTI0YjQ=|1504070278|8ec4087081442939b97fcb032f3ffde8b5f0c850"; d_c0="AGDCBnN4TAyPTgLjlyxNipPlWNDY6bSQaxI=|1504070278"; z_c0=Mi4xTzFsNEFnQUFBQUFBWU1JR2MzaE1EQmNBQUFCaEFsVk5qTmZOV1FBTmwwWW5jT1RSTW1IM29PNHowM0hhMFJJMGZ3|1504070284|c9af10b7d8082fd488412ba383ca4d412b73be37; __utma=51854390.1389235150.1504070270.1504156423.1504340999.5; __utmz=51854390.1504340999.5.5.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/40551563; __utmv=51854390.100-1|2=registration_date=20160112=1^3=entry_date=20160112=1; aliyungf_tc=AQAAAFXCBUyC1AQAu/UbdZtCduGYB+G+; _xsrf=125593de-f137-4018-a5c0-94e4a4dd73fb',
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
