# !/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys
import requests
import re
from urllib.request import urlretrieve
from threading import Thread

Threads = []

def CheckArgs():
    if(len(sys.argv) < 2):
        print('Usage: python3 getBaiduPics.py [Word] [Pages=1]')
        print('The pictures will be saved in the [Word] folder.')
        return False
    return True

def decode(url):
    str_table = {
        '_z2C$q': ':',
        '_z&e3B': '.',
        'AzdH3F': '/'
    }

    char_table = {
        'w': 'a',
        'k': 'b',
        'v': 'c',
        '1': 'd',
        'j': 'e',
        'u': 'f',
        '2': 'g',
        'i': 'h',
        't': 'i',
        '3': 'j',
        'h': 'k',
        's': 'l',
        '4': 'm',
        'g': 'n', 
        '5': 'o',
        'r': 'p',
        'q': 'q',
        '6': 'r',
        'f': 's',
        'p': 't',
        '7': 'u',
        'e': 'v',
        'o': 'w',
        '8': '1',
        'd': '2',
        'n': '3',
        '9': '4',
        'c': '5',
        'm': '6',
        '0': '7',
        'b': '8',
        'l': '9',
        'a': '0'
    }

    char_table = {ord(key): ord(value) for key, value in char_table.items()}
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)



def Download(urls):
    if(os.path.exists(sys.argv[1]) == False):
        os.mkdir(sys.argv[1]);
    for url, filename in urls.items():
        filepath = os.path.join(sys.argv[1], '%s' % filename)
        print('downloading ', url)
        try :
            urlretrieve(url, filepath)
        except Exception as e:
            print('\nThe request has been rejected. The url is: '+url+'\n')
    return 

def Request(param):
    urls = {}
    searchurl = 'http://image.baidu.com/search/acjson'
    response = requests.get(searchurl, params=param)
    data = response.json()['data']
    for x in data[:len(data)-1]:
        imgUrl = decode(x['objURL'])
        tail = re.findall(r'.*\/(.*)', imgUrl)[0]
        name = x['fromPageTitleEnc'].encode(response.encoding).decode('utf-8') + tail
        name = re.sub(r'\s+', '', name)
        urls[imgUrl] = name
    t = Thread(target = Download, args = (urls, ))
    Threads.append(t)

def Search():
    params = {
        'tn':'resultjson_com',
        'ipn':'rj',
        'ct':'201326592',
        'queryWord':sys.argv[1],
        'cl':'2',
        'lm':'-1',
        'ie':'utf-8',
        'oe':'utf-8',
        'st':'-1',
        'z':'',
        'ic':'0',
        'word':sys.argv[1],
        'face':'0',
        'istype':'2',
        'qc':'',
        'nc':'1',
        'fr':'',
        'rn':'30',
        'gsm':'1e',
        };
    
    if(len(sys.argv) == 3):
        pages = int(sys.argv[2])
    else:
        pages = 1
    for i in range(pages):
        params['pn'] = '%d' % i
        Request(params)
    return 

if __name__ == '__main__':
    if(CheckArgs() == False):
        sys.exit(-1)
    Search()
    for t in range(len(Threads)):
        Threads[t].start()
    for t in range(len(Threads)):
        Threads[t].join()
    print('Pictures have been saved in /'+sys.argv[1]+' fold!'）
