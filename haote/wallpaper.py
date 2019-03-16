#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-16 20:45:25
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os
import time
import requests
from threading import Thread
from bs4 import BeautifulSoup as Soup

headers = {
	'Referer': 'https://www.haote.com/game/pubg/bizhi/',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
}

def get_links(key):
	p = 1
	timestamp = int(round(time.time() * 1000))
	while True:
		url = f'https://www.haote.com/jingpin/bizhilist?page={p}&ajax=1&url=pubg&tagurl={key}&timestamp={timestamp}'
		r = requests.get(url, headers = headers)

		if key == '164':
			table = Soup(r.text, 'html5lib').find_all('li')
		else:
			table = Soup(r.text, 'html5lib').find_all('div')
		
		if not table:
			return

		links = []
		for x in table:
			link = x.span.a['href']
			links.append(link)

		download(key, links)

		p += 1

def download(key, links):
	for x in links:
		name = x.split('/')[-1]
		print(key, name)
		if os.path.exists(f'wallpaper/{key}/{name}'):
			continue

		r = requests.get(x, headers = headers)
		
		with open(f'wallpaper/{key}/{name}', 'wb') as f:
			f.write(r.content)

if __name__ == '__main__':
	if not os.path.exists('wallpaper'):
		os.mkdir('wallpaper')
	
	page = ['164', '165', '166', '167']
	
	for x in page:
		if not os.path.exists(f'wallpaper/{x}'):
			os.mkdir(f'wallpaper/{x}')

	threads = []
	
	for x in page:
		t = Thread(target=get_links, args=(x,))
		threads.append(t)

	for x in threads:
		x.start()

	for x in threads:
		x.join()