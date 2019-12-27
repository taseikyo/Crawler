#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-19 09:52:36
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import csv
from glob import glob


def convert():
    '''take out the author and title information & save as txt'''
    for x in glob('../csv/*'):
        n_list = []
        with open(x, encoding='utf-8') as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                n_list.append([row[0], row[3]])
        with open(f'{x}.txt', 'w', encoding='utf-8', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(n_list)

def get9books():
    '''count >= 9.0 book'''
    n_list = []
    for x in glob('../csv/*'):
        count = 0
        with open(x, encoding='utf-8') as f:
            f_csv = csv.reader(f)
            for i, row in enumerate(f_csv):
                if i == 0:
                    continue
                count += 1 if float(row[1]) >= 0 else 0
            n_list.append([x.split('\\')[-1].split('.')[0], count])
    with open(f'catalog.csv', 'w', encoding='utf-8', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(n_list)

def top10books():
    n_list = []
    for x in glob('../csv/*'):
        with open(x, encoding='utf-8') as f:
            f_csv = csv.reader(f)
            for i, row in enumerate(f_csv):
                if i == 0:
                    continue
                n_list.append([row[0], row[1], row[3], row[5]])
    n_list = sorted(n_list, key=lambda x: x[1], reverse=True)[:11]
    
    for i, _ in enumerate(n_list):
        n_list[i].insert(0, i+1)
        n_list[i][1] = f'[{n_list[i][1]}](https://book.douban.com/subject/{n_list[i][-1]}/?from=tag_all)'
        n_list[i].pop()

    with open(f'top10.csv', 'w', encoding='utf-8', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(n_list)

def top10book(name):
    n_list = []
    for x in glob(f'../csv/{name}.csv'):
        with open(x, encoding='utf-8') as f:
            f_csv = csv.reader(f)
            for i, row in enumerate(f_csv):
                if i == 0:
                    continue
                n_list.append([row[0], row[1], row[3], row[5]])
    n_list = sorted(n_list, key=lambda x: x[1], reverse=True)[:10]
    
    for i, _ in enumerate(n_list):
        n_list[i].insert(0, i+1)
        n_list[i][1] = f'[{n_list[i][1]}](https://book.douban.com/subject/{n_list[i][-1]}/?from=tag_all)'
        n_list[i].pop()

    with open(f'top10-{name}.csv', 'w', encoding='utf-8', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(n_list)

if __name__ == '__main__':
    top10book('历史')