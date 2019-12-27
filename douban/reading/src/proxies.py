#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-18 09:37:02
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import requests
from bs4 import BeautifulSoup as Soup

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}

def get_proxies(pages=1):
    '''get proxies according to {page}'''
    valid_ip = []
    for page in range(1, pages+1):
        url = f'https://www.xicidaili.com/nn/{page}'
        r = requests.get(url=url, headers=HEADER)
        soup = Soup(r.text, 'lxml')
        ip_list = soup.find(id='ip_list').find_all('tr')
        for ip_info in ip_list:
            td_list = ip_info.find_all('td')
            if td_list:
                ip_address = td_list[1].text
                ip_port = td_list[2].text
                if test_ip(ip_address, ip_port):
                    valid_ip.append(f'{ip_address}:{ip_port}')
                    print(valid_ip[-1])
    save_ip(valid_ip)

def test_ip(addr, port):
    '''test if ip(addr: port) is valid'''
    url = 'https://www.ip.cn/'
    ip_url_next = f'://{addr}:{port}'
    proxies = {'http': f'http{ip_url_next}', 'https': f'https{ip_url_next}'}
    try:
        r = requests.get(url, headers=HEADER, proxies=proxies, timeout=3)
    except Exception as e:
        return False
    return True

def save_ip(ip_list):
    with open('proxies.txt', 'w') as f:
        f.write('\n'.join(ip_list))

if __name__ == '__main__':
    get_proxies()
