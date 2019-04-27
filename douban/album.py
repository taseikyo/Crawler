#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-27 16:04:26
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os
import requests
from threading import Thread
from bs4 import BeautifulSoup as Soup
from urllib.request import urlretrieve

'''
一个多线程爬取豆瓣相册的小爬虫

参数: 相册 id
'''

def main(aid, page = 0):
	print(f'retrieve page-{page}...')

	headers = {
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
	}
	url = f'https://www.douban.com/photos/album/{aid}/?start={page*18}'
	r = requests.get(url, headers = headers)
	soup = Soup(r.text, 'html5lib')
	grid = soup.find('div', {'class', 'photolst'})
	cells = grid.find_all('div', {'class', 'photo_wrap'})
	if not cells: return False
	pids = []
	for x in cells:
		link = x.a.img['src']
		pids.append(link.split('/')[-1].split('.')[0])
	Thread(target = download, args = (aid, pids)).start()
	main(aid, page+1)

def download(aid, pids):
	if not os.path.exists(aid):
		os.mkdir(aid)
	
	for p in pids:
		url = f'https://img3.doubanio.com/view/photo/l/public/{p}.jpg'
		try:
			urlretrieve(url, f'{aid}/{p}.jpg')
		except:
			print(f'fail to download {p}.jpg...')

if __name__ == '__main__':
	aid = '26081877'
	main(aid)