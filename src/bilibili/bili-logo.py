#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-17 18:36:13
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : Python3.7


import os
import time
import threading
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as Soup

"""
download bilibili logo images
"""


def download(html):
    """
    下载对应页面的 logo
    """
    soup = Soup(html, "html5lib")
    try:
        logo = soup.find("img", {"class": "logo-img"})["src"]
    except Exception as e:
        print(e)
        return

    name = logo.split("/")[-1]
    if not os.path.exists("images"):
        os.mkdir("images")
    if os.path.exists(f"images/{name}"):
        return

    r = requests.get(f"http:{logo}")
    print(f"downloading {name}...")
    with open(f"images/{name}", "wb") as f:
        f.write(r.content)


def browser(urls):
    """
    发现除了首页 logo 直接在 html 中
    其他都是通过 js 生成的 url，看不太懂怎么生成的
    干脆直接用 selenium 抓算了 :3
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(8)
    for url in urls:
        driver.get(url)
        threading.Thread(target=download, args=(driver.page_source,)).start()
        time.sleep(1.5)
    driver.quit()


if __name__ == "__main__":
    urls = [
        "https://www.bilibili.com/",
        "https://www.bilibili.com/v/douga/",
        "https://www.bilibili.com/v/music/",
        "https://www.bilibili.com/v/dance/",
        "https://www.bilibili.com/v/technology/",
        "https://www.bilibili.com/v/life/",
        "https://www.bilibili.com/v/fashion/",
        "https://www.bilibili.com/v/ent/",
        "https://www.bilibili.com/cinema/",
        "https://www.bilibili.com/anime/",
        "https://www.bilibili.com/guochuang/",
        "https://www.bilibili.com/v/game/",
        "https://www.bilibili.com/v/digital/",
        "https://www.bilibili.com/v/kichiku/",
        "https://www.bilibili.com/v/information/",
        "https://www.bilibili.com/v/cinephile/",
        "https://www.bilibili.com/v/life/funny",
        "https://www.bilibili.com/v/life/animal",
        "https://www.bilibili.com/v/life/food",
        "https://www.bilibili.com/v/game/stand_alone",
    ]
    browser(urls)
