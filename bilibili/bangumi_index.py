#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-22 22:37:35
# @Author  : Lewis Tian (2471740600@qq.com | lewis.smith.tian@gmail.com)
# @Link    : https://lewistian.github.io/
# @Version : Python3.5

import requests
import optparse
import json
from pprint import pprint

data  = {
	'page':1,			# 第几页
	'page_size':20,		# 每页的数量
	'version':0, 		# 类型： 全部 正片 剧场版 其他 [0 - 4]
	'is_finish':0,		# 状态： 全部 完结 连载 [0 2 1]
	'start_year':0, 	# 时间： 全部 某一年 [0 xxxx]
	'tag_id':'',		# 风格
	'index_type':1,		# 排序方式: 更新时间 追番人数 开播时间 [0 - 2]
	'index_sort':0,		# 排序类型: 递减 递增 [0 - 1]
	'area':0,			# 地区: 全部 日本 美国 其他 [0 2 3 4]
	'quarter':0   		# 季度： 全部 1月 4月 7月 10月 [0 - 4]
}

class Anime(requests.Session):
	"""docstring for Anime"""
	def __init__(self, options):
		super(Anime, self).__init__()
		self.api = 'https://bangumi.bilibili.com/web_api/season/index_global'
		self.parse(options)

	def parse(self, options):
		self.b_type = options.b_type
		self.b_area = options.b_area		
		self.b_state = options.b_state
		self.b_year = options.b_year
		self.season = options.season
		self.b_style = options.b_style
		self.index_type = options.index_type
		self.index_sort = options.index_sort

	def run(self):
		r = self.get(self.api, params = data)
		pprint(r.json())

def main():
	parser = optparse.OptionParser('usage: [-t <type> | -a <area> | -e <state> | -m <time> |\t\n -s <season> | --tag <style> | --index_type <index_type> | --index_sort <index_sort>]')
	parser.add_option('-t', dest='b_type', type='int', help='1.全部 2.正片 3.剧场版 4.其他')
	parser.add_option('-a', dest='b_area', type='int', help='0.全部 2.日本 3.美国 4.其他')
	parser.add_option('-e', dest='b_state', type='int', help='0.全部 1.连载 2.完结 ')
	parser.add_option('-y', dest='b_year', type='string', help='更新年份')
	parser.add_option('-s', dest='season', type='int', help='0.全部 1.1月 2.4月 3.7月 4.10月')
	parser.add_option('--tag', dest='b_style', type='string', default='', help='风格')
	parser.add_option('--index_type', dest='index_type', type='int', help='0.更新时间 1.追番人数 2.开播时间')
	parser.add_option('--index_sort', dest='index_sort', type='int', help='0.递减 1.递增')
	(options, args) = parser.parse_args()
	Anime(options).run()


if __name__ == '__main__':
	main()