#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-02 17:23:17
# @Author  : Lewis Tian (2471740600@qq.com | lewis.smith.tian@gmail.com)
# @Link    : https://lewistian.github.io/
# @Version : Python3.5

import requests
from bs4 import BeautifulSoup as BS
import time

class Music(requests.Session):
	"""网易云歌曲下载爬虫"""
	def __init__(self):
		super(Music, self).__init__()

	def __del__(self):
		self.close()

	def get_album_list(self, list_id):
		"""根据 list_id 下载歌单所有歌"""
		List = {}
		url = 'http://music.163.com/playlist?id={}'.format(list_id)
		self.headers.update({
		    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
		    'Referer':'http://music.163.com/',
		})
		r = self.get(url).text
		soup = BS(r, 'html5lib').find('ul', {'class', 'f-hide'}).findAll('li')
		for x in soup:
			List[x.a['href'].split('=')[1]] = x.a.text # k: v = sid: name
		for k, v in List.items():
			self.download(k, v)
			time.sleep(1.5)

	def download(self, sid, name):
		"""根据 sid 下载歌曲并保存为 name.mp3"""
		url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(sid)
		self.headers.update({
		    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
		    'Upgrade-Insecure-Requests':'1',
		    'Referer':url,
		})
		r = self.get(url)
		print("begin to save {}.mp3...".format(name))
		with open(name+'.mp3', 'wb') as f:
			f.write(r.content)
		print("{}.mp3 has been saved...\n==================".format(name))

if __name__ == '__main__':
	m = Music()
	# m.download(33206214, '小幸运')
	m.get_album_list(2120700410)