#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-17 18:09:33
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os
import time
import csv
from random import randint
from concurrent import futures
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup as Soup


UAS = []
PROXIES = []
MAX_TRY_TIMES = 10
USE_PROXYT = False

def save_as_csv(book_lists, book_tag_lists):
    '''save data as excel'''
    header = ['书名', '评分', '评价人数', '作者', '出版社', '书的id']
    for index, book_list in enumerate(book_lists):
        filename = f'../csv/{book_tag_lists[index]}.csv'
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(header)
            f_csv.writerows(book_list)

def get_people_num(url):
    ''' get rating people nums'''
    # 'http://book.douban.com/subject/6082808/?from=tag_all'
    try:
        if USE_PROXYT:
            r = requests.get(url, headers=UAS[randint(0, len(UAS)-1)],
                             proxies=PROXIES[randint(0, len(PROXIES)-1)])
        else:
            r = requests.get(url, headers=UAS[randint(0, len(UAS)-1)])
    except Exception as e:
        print('get_people_num', url, e)
    soup = Soup(r.text, 'html5lib')
    people_num = soup.find('a', {'class': 'rating_people'}).span.string.strip()

    return people_num

def book_spider(book_tag):
    '''get books infos'''
    page_num = 0
    book_list = []
    try_times = 0

    while True:
        # https://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book?start=0
        print(f'get tag: {book_tag} page: {page_num} try: {try_times+1}..')

        url = f'http://www.douban.com/tag/{quote(book_tag)}/book?start={page_num*15}'
        time.sleep(randint(500, 1000)/1000)

        try_times += 1
        if try_times > MAX_TRY_TIMES:
            break

        # Last Version
        try:
            if USE_PROXYT:
                r = requests.get(url, headers=UAS[randint(0, len(UAS)-1)],
                                 proxies=PROXIES[randint(0, len(PROXIES)-1)])
            else:
                r = requests.get(url, headers=UAS[randint(0, len(UAS)-1)])
        except Exception as e:
            print('book_spider', book_tag, page_num, e)
            continue

        soup = Soup(r.text, 'html5lib')
        list_soup = soup.find('div', {'class': 'book-list'})

        if not list_soup:
            continue
        elif not list_soup or len(list_soup) <= 1:
            break # Break when no informatoin got after MAX_TRY_TIMES times requesting

        for book_info in list_soup.find_all('dd'):
            temp = book_info.find('a', {'class':'title'})
            title = temp.string.strip()
            book_url = temp['href']
            desc = book_info.find('div', {'class':'desc'}).string.strip()
            # desc_list: author1, author2...authorn, press, pub_time, price
            desc_list = desc.split('/')

            try:
                author_info = f'{"/".join(desc_list[0:-3])}'
            except:
                author_info = '暂无'
            try:
                pub_info = f'{"/".join(desc_list[-3:])}'
            except:
                pub_info = '暂无'
            try:
                rating = book_info.find('span', {'class':'rating_nums'}).string.strip()
            except:
                rating = '0.0'
            try:
                people_num = get_people_num(book_url)
            except:
                people_num = '0'
            try:
                # https://book.douban.com/subject/{book_id}/?from=tag_all
                book_id = book_url.split('/')[-2]
            except:
                book_id = '0'

            book_list.append([title, rating, people_num, author_info, pub_info, book_id])
            try_times = 0 # set 0 when got valid information
        page_num += 1

    return book_list

def do_spider(book_tag_lists):
    book_lists = []

    if isinstance(book_tag_lists, str):
        book_tag_lists = [book_tag_lists]

    for book_tag in book_tag_lists:
        book_list = book_spider(book_tag)
        book_list = sorted(book_list, key=lambda x: x[1], reverse=True)
        book_lists.append(book_list)

    save_as_csv(book_lists, book_tag_lists)

def prepare_spider(book_tag_lists):
    with futures.ThreadPoolExecutor(len(book_tag_lists)) as executor:
        executor.map(do_spider, book_tag_lists)

def read_ip_lists():
    '''read all proxy from proxies.txt, you can run proxies.py to get valid ip'''
    global PROXIES
    with open('proxies.txt') as f:
        ip_list = f.readlines()
    for ip in ip_list:
        ip = ip.replace("\n", "")
        ip_url_next = f'://{ip}'
        proxies = {'http': f'http{ip_url_next}', 'https': f'https{ip_url_next}'}
        PROXIES.append(proxies)

def read_uas():
    '''read all ua from uas.txt, you can add more ua to the text file'''
    global UAS
    with open('uas.txt') as f:
        ua_list = f.readlines()
    for ua in ua_list:
        head = {}
        head['User-Agent'] = ua.replace('\n', '')
        UAS.append(head)

def main():
    '''multi-thread to reduce time'''
    book_tag_listss = [
        ['心理', '判断与决策', '算法', '数据结构', '经济', '历史'],
        ['传记', '哲学', '编程', '创业', '理财', '社会学', '佛教'],
        ['思想', '科技', '科学', 'web', '股票', '爱情', '两性'],
        ['计算机', '机器学习', 'linux', 'android', '数据库', '互联网'],
        ['数学'],
        ['摄影', '设计', '音乐', '旅行', '教育', '成长', '情感', '育儿', '健康', '养生'],
        ['商业', '理财', '管理'],
        ['名著'],
        ['科普', '经典', '生活', '心灵', '文学'],
        ['科幻', '思维', '金融'],
        ['个人管理', '时间管理', '投资', '文化', '宗教']
    ]

    if not os.path.exists('../csv'):
        os.mkdir('../csv')

    read_uas()

    if USE_PROXYT:
        read_ip_lists()

    with futures.ThreadPoolExecutor(len(book_tag_listss)) as executor:
        executor.map(do_spider, book_tag_listss)

if __name__ == '__main__':
    main()
