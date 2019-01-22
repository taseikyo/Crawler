#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-22 09:56:52
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os
import math
import requests
import re
import time
import threading
from urllib.request import urlretrieve

'''
从视频下方的回复者中提取挂件
api：https://api.bilibili.com/x/v2/reply?callback=jQuery172016532967742963667_1548121853369&jsonp=jsonp&pn=1&type=1&oid={$av}&sort=0&_={$timestamp}
json
	data
		replies
			i[0,2,3...19]
				member
					pendant
						image
						name
挂件的嵌套格式如上所示
'''

def pendant(url):
	has_more = True
	pn = 1
	while has_more:
		print(f'retrieving {url} page {pn}...')
		av = re.findall(r'\d+', url)[0]
		api = f'https://api.bilibili.com/x/v2/reply?callback=&jsonp=jsonp&pn={pn}&type=1&oid={av}&sort=0&_={int(time.time()*1000)}'
		headers = {
			'Host': 'api.bilibili.com',
			'Referer': url,
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
		}
		r = requests.get(api, headers = headers)
		try:
			replies = r.json()['data']['replies']
		except Exception as e:
			print(e)
			return
		data = []
		for x in replies:
			p = x['member']['pendant']
			image = p['image']
			name = p['name']
			if image:
				d = {}
				d['image'] = image
				d['name'] = name
				data.append(d)
		threading.Thread(target=download, args=(data, )).start()
		page = r.json()['data']['page']
		has_more = page['num'] < math.ceil(page['count']/page['size'])
		pn += 1
		time.sleep(1)

def download(data):
	for x in data:
		name = x['name']
		image = x['image']
		if os.path.exists(f'bili-pendant/{name}.png'):
			continue
		print(f'downloading {name} {image}')
		urlretrieve(image, f'bili-pendant/{name}.png')

if __name__ == '__main__':
	if not os.path.exists('bili-pendant'):
		os.mkdir('bili-pendant')
	with open('bili-pendant.txt') as f:
		data = f.readlines()
	for x in data:
		pendant(x.replace('\n', ''))