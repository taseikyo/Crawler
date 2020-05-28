#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-05-19 21:02:01
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : Python3.8

"""
download weibo user's pictures (original image)
"""


import os
import re
import sys
import time
import argparse
from urllib import request as urequest
import requests


HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "referer": "https://m.weibo.cn",
}


def weibo_user(uid, since_id="", pages=5):
    """
    get user pictures according to the `uid`

    @uid: user id
    @since_id: to get next page
    @pages: how many pages you want to get
    """
    url = "https://m.weibo.cn/api/container/getIndex"
    params = {
        "type": "uid",
        "value": uid,
        "containerid": f"107603{uid}",
    }

    if since_id:
        params["since_id"] = since_id

    r = requests.get(url, headers=HEADERS, params=params)
    try:
        data = r.json()["data"]
    except Exception as e:
        print(e)
        return
    cards = data["cards"]
    pic_urls = []
    for card in cards:
        """
        type: 9 -> video/picture; 11 -> interested perple;
        nums: 0 -> video
        """
        card_type = card["card_type"]
        if card_type == 11:
            continue

        nums = card["mblog"]["pic_num"]
        if nums == 0:
            continue

        pics = card["mblog"]["pics"]
        for pic in pics:
            pic_url = pic["large"]["url"].split("/")[-1]
            pic_urls.append(pic_url)

    try:
        since_id = data["cardlistInfo"]["since_id"]
    except Exception as e:
        print(e)
        return

    download(uid, pic_urls)

    pages -= 1
    if not pages:
        return

    time.sleep(1.5)
    weibo_user(uid, since_id, pages)


def weibo_single(mid):
    """
    get one weibo picture according to `mid`

    @mid: weibo id
    """
    url = f"https://m.weibo.cn/detail/{mid}"
    r = requests.get(url, headers=HEADERS)
    try:
        pics = re.findall(r"\"pic_ids\": \[(.*?)\]", r.text, re.S)[0]
        uid = re.findall(r"u/(\d+)\?uid", r.text)[0]
    except Exception as e:
        print(e)
        return
    # print(r.text)
    pics = pics.replace(" ", "").replace("\n", "").strip().split(",")
    pic_urls = [f"{pic[1:-1]}.jpg" for pic in pics]

    download(uid, pic_urls)


def download(uid, pic_urls):
    """
    download pictures and save them to `uid` folder

    @uid: the folder to save the pics
    @pic_urls: pictures name (xxxxx.jpg)
    """
    if not os.path.exists(uid):
        os.mkdir(uid)

    for pic in pic_urls:
        if os.path.exists(f"{uid}/{pic}"):
            continue

        url = f"https://wx1.sinaimg.cn/large/{pic}"
        print(f"{' '*7} {pic}...", end="")
        urequest.urlretrieve(url, filename=f"{uid}/{pic}", reporthook=report)


def report(count, blockSize, totalSize):
    """
    show the downloading prograss
    """
    downloadedSize = count * blockSize
    percent = int(downloadedSize * 100 / totalSize)
    if percent >= 100:
        percent = 100
        print(f"\r{percent:6.2f} ")
    else:
        print(f"\r{percent:6.2f} ", end=" ")


def main():
    """
    repalce optparse with argparse
    """
    parser = argparse.ArgumentParser(
        "usage: -u <user id> -p <pages> | -w <single weibo mid>"
    )
    parser.add_argument(
        "-u", "--user_id", dest="user_id", type=str, help="the user's weibo id",
    )
    parser.add_argument(
        "-p",
        "--pages",
        dest="pages",
        type=int,
        help="how many pages you want to download",
        default=5,
    )
    parser.add_argument(
        "-w", "--weibo_mid", dest="weibo_mid", type=str, help="one single weibo id"
    )

    args = parser.parse_args()
    user_id = args.user_id
    pages = args.pages
    weibo_mid = args.weibo_mid

    if (not user_id) and (not weibo_mid):
        print(f"try `python3 {__file__} --help` for help")
    elif user_id:
        weibo_user(user_id, pages=pages)
    else:
        weibo_single(weibo_mid)


if __name__ == "__main__":
    main()
