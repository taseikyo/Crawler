#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-28 12:23:34
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io/
# @Version : Python3.5

import requests
import optparse
from collections import namedtuple
from bs4 import BeautifulSoup as BS
import csv
import os

"""
前端: fe
后端: be
移动: mobile
数据库: data
人工智能: ai
云计算&大数据: cb
运维&测试: op
UI设计: photo
"""

header = ['m_name','m_people','m_level','m_cover','m_label','m_desc']
Muke = namedtuple('Muke', header)
categories = ['fe','be','mobile','data','ai','cb','op','photo']

class Course(requests.Session):
	"""www.imooc.com course"""
	def __init__(self, m_type, m_cate):
		super(Course, self).__init__()
		self.m_type = m_type
		self.m_cate = m_cate
		self.api = 'https://www.imooc.com/course/list'


	def close(self):
		self.close()

	def run(self):
		if not self.m_type or self.m_type == 1:
			self.run1()
		elif self.m_type == 2:
			self.run2()
		elif self.m_type == 3:
			self.run3(self.m_cate)
		else:
			print("'type' input error!\ninput python course.py -h for help.")

	def run1(self):
		print('Strating to get all data from www.muke.com...')
		Course = []
		self.headers.update({
			'Host':'www.imooc.com',
			'Referer':self.api,
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
			})
		print('page 1...')
		r = self.get(self.api)
		soup = BS(r.text, 'html5lib')
		pages = int(soup.find('div', {'class', 'page'}).findAll('a')[-1]['href'].split('=')[-1])
		Course += self.parse(soup)
		for p in range(2, pages+1):
			print('page {}...'.format(p))
			r = self.get(self.api+'?page='+str(p))
			soup = BS(r.text, 'html5lib')
			Course += self.parse(soup)
		self.saveAsCsv('all', Course)

	def run2(self):
		for c in categories:
			print('Strating to get all data from www.muke.com/{}...'.format(c))
			api = self.api+'?c='+c
			Course = []
			self.headers.update({
				'Host':'www.imooc.com',
				# 'Referer':api,
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
				})
			print('page 1...')
			r = self.get(api)
			soup = BS(r.text, 'html5lib')
			try:
				pages = int(soup.find('div', {'class', 'page'}).findAll('a')[-1]['href'].split('=')[-1])
			except:
				pages = 1
			Course += self.parse(soup)
			for p in range(2, pages+1):
				print('page {}...'.format(p))
				r = self.get(api+'&page='+str(p))
				soup = BS(r.text, 'html5lib')
				Course += self.parse(soup)
			self.saveAsCsv(c+'_batch', Course)

	def run3(self, m_cate):
		print('Strating to get all data from www.muke.com/{}...'.format(m_cate))
		self.api += '?c='+m_cate
		print(self.api)
		Course = []
		self.headers.update({
			'Host':'www.imooc.com',
			# 'Referer':self.api,
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
			})
		print('page 1...')
		r = self.get(self.api)
		soup = BS(r.text, 'html5lib')
		pages = int(soup.find('div', {'class', 'page'}).findAll('a')[-1]['href'].split('=')[-1])
		Course += self.parse(soup)
		for p in range(2, pages+1):
			print('page {}...'.format(p))
			r = self.get(self.api+'&page='+str(p))
			soup = BS(r.text, 'html5lib')
			Course += self.parse(soup)
		self.saveAsCsv(m_cate, Course)

	def parse(self, soup):
		tmp_course = []
		courses = soup.find('div', {'class', 'moco-course-list'}).findAll('div', {'class', 'course-card-container'})
		for x in courses:
			name = x.find('h3', {'class', 'course-card-name'}).text
			print(name)
			cover = x.find('img')['data-original']
			tmp = x.find('div', {'class', 'course-card-info'}).findAll('span')
			level = tmp[0].text
			people = tmp[1].text
			desc = x.find('p', {'class', 'course-card-desc'}).text
			try:
				tmp = x.find('div', {'class', 'course-label'}).findAll('label')
				label = []
				for i in tmp:
					label.append(i.text)
			except:
				label = ['NULL']
			muke = Muke(
				name,
				people,
				level,
				cover,
				label,
				desc
			)
			tmp_course.append(muke)
		return tmp_course

	def saveAsCsv(self, name, data):
		print('Strating to save data as csv file...')
		if not os.path.exists('csv'):
			os.mkdir('csv')
		with open('csv/{}.csv'.format(name), 'w', encoding='utf-8') as f:
			f_csv = csv.writer(f)
			f_csv.writerows(data)
		print('csv/{}.csv has been created successfully...'.format(name))

def main():
	parser = optparse.OptionParser('usage: [-t <type> | - c <category>]')
	parser.add_option('-t', dest='m_type', type='int', help='1.全部 2.循环种类全部 3.输入某一种类')
	parser.add_option('-c', dest='m_cate', type='string', help='category')
	(opts, args) = parser.parse_args()
	Course(opts.m_type, opts.m_cate).run()

if __name__ == '__main__':
	main()