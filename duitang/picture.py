#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-13 16:17:18
# @Author  : Lewis Tian (chasetichlewis@gmail.com)
# @GitHub  : https://github.com/LewisTian
# @Version : Python3.5

import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import quote
import time
import os

class DuiTang(requests.Session):
    """根据关键字下载 堆糖 图片"""
    def __init__(self, kw, page = 1):
        super(DuiTang, self).__init__()
        self.kw = quote(kw)
        self.page = page
        if not os.path.exists('img'):
            os.mkdir('img')

    def __del__(self):
        self.close()

    def run(self):
        self.headers.update({
            "authority":"www.duitang.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
            "upgrade-insecure-requests":"1",
            "referer": "https://www.duitang.com/search/?kw={}&type=feed&from=webhome".format(self.kw),
        })
        next_start = 0
        for i in range(0, self.page * 5 + 1):
            url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={kw}&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum&_type=&start={start}&_={time}'.format(kw = self.kw, start = next_start, time = self.timestamp())
            r = self.get(url)
            data = r.json()['data']
            next_start = data['next_start']
            pics = data['object_list']
            for x in pics:
                # albumId = x['album']['id'] # 专辑id
                # albumCount = x['album']['count'] # 专辑照片数
                # albumStore = x['album']['favorite_count'] # 专辑收藏数
                # albumLike = x['album']['like_count'] # 专辑点赞数
                # albumName = x['album']['name'] # 专辑名
                # userName = x['sender']['username']
                # userId = x['sender']['id']
                # picStore = x['favorite_count'] # 图片收藏数
                # picLike = x['like_count']
                # picId = x['id']
                # picMsg = x['msg']
                picSrc = x['photo']['path'] # 图片链接
                print(picSrc)
            time.sleep(5)

    def timestamp(self):
        return int(round(time.time() * 1000))

    def download(self, src):
        name = src.split('/')[-1]
        r = self.get(src)
        with open('img/'+name, 'wb') as f:
            f.write(r.content)

    def album(self, id):
        """下载专辑所有图片"""
        pass

if __name__ == '__main__':
    d = DuiTang('古风')
    d.run()