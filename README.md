# Python3 爬虫合集![python version](https://img.shields.io/badge/python-3.5-brightgreen.svg)
> 人生苦短, 我用Python!

## Contents
<table>
	<tr>
		<td><a href="#bilibili">Bilibili</a></td>
		<td><a href="#豆瓣">豆瓣</a></td>
		<td><a href="#优酷">优酷</a></td>
	</tr>
	<tr>
		<td><a href="#pixiv">Pixiv</a></td>
		<td><a href="#微博">微博</a></td>
		<td><a href="#知乎">知乎</a></td>
	</tr>
	<tr>
		<td><a href="#百度">百度</a></td>
		<td><a href="#微软">微软</a></td>
		<td><a href="#其他">其他</a></td>
	</tr>
</table>

## Bilibili
### [爬取弹幕并保存到txt中](https://github.com/LewisTian/Python/blob/master/bilibili/danmu.py)
- [Usage]: `python danmu.py $url`
- [Example]: `python danmu.py https://www.bilibili.com/video/av9933492/`

## 豆瓣
### [爬取豆瓣电影top250并存到Excel中](https://github.com/LewisTian/Python/blob/master/douban/MovieTop250.py)
<div align="center">
	<img src="douban/movieTop250.png" alt="douban" width="500">
</div>

## 优酷
### [爬取优酷视频弹幕](https://github.com/LewisTian/Python/blob/master/youku/danmu.py)
- 使用前记得修改 `data` 和 `headers` 中的 `Referer` 数据，我填入的是[火影第一集](http://v.youku.com/v_show/id_XNTQwMTgxMTE2.html)的弹幕请求数据
- [视频介绍](https://www.bilibili.com/video/av13784309/)

### [爬取优酷首页轮换图](https://github.com/LewisTian/Python/blob/master/youku/screen_pics.py)
<div align="center">
	<img src="https://i.loli.net/2017/11/07/5a0155cebc280.png" alt="youku" width="500">
</div>

## Pixiv
### [爬取首页的轮换图片](https://github.com/LewisTian/Python/blob/master/pixiv/cover.py)
<div align="center">
	<img src="pixiv/pixiv.png" alt="pixiv首页轮换图" width="500">
</div>

## 微博
### [爬取微博亚洲新歌榜top50并存到Excel中](https://github.com/LewisTian/Python/blob/master/weibo/NewSongTop50.py)
<div align="center">
	<img src="weibo/weibo.png" alt="微博亚洲新歌榜" width="450">
</div>

## 知乎
### [爬取知乎回答图片](https://github.com/LewisTian/Python/blob/master/zhihu/image.py)
- 使用前需要更新问题 `id`, 填入 `Cookie`, `include` 应该不需要更新

### [爬取知乎异步加载页面数据(第二页及之后)](https://github.com/LewisTian/Python/blob/master/zhihu/ajax_page.py)
- 返回未验证方式是因为没有给headers传递 `X-API-VERSION`, `X-UDID`, `authorization` 等参数
- 问题来自知乎一位朋友问我, 因此做的比较粗糙, 没有详细提取数据, 仅将答主提取出来
- 得到的一些答主 [数据](https://github.com/LewisTian/Python/blob/master/zhihu/ajax_page.txt)

## 百度
### [爬取贴吧图片并保存到对应pid文件夹下](https://github.com/LewisTian/Python/blob/master/baidu/getTiebaPics.py)
- [Usage]: `python danmu.py $pid`
- [Example]: `python getTiebaPics.py 2271504759`

### [爬取百度图片](https://github.com/LewisTian/Python/blob/master/baidu/getBaiduPics.py)
- [Usage]: `python3 getBaiduPics.py [Word] [pages = 1]`
- [Example]: `python3 getBaiduPics.py 猫 30`
- 注: 图片将保存在关键词的同名目录下。

## 微软
### [爬取bing主页背景图](https://github.com/LewisTian/Python/blob/master/bing/cover.py)
<div align="center">
	<img src="bing/Piraputanga_ZH-CN13303102627_1920x1080.jpg" alt="bing" width="600">
</div>
<div align="center">
	<img src="bing/QQ截图20171130191346.jpg" alt="screenshot" width="600">
</div>

## 其他
### [爬取「ONE · 一个」的插图](https://github.com/LewisTian/Python/blob/master/one/image.py)
- [「ONE · 一个」](http://www.wufazhuce.com/)

### 爬取[煎蛋网](http://jandan.net/ooxx/)妹子图
- [问题](http://bbs.fishc.com/thread-98098-1-1.html)来自[鱼C互助区](http://bbs.fishc.com/bestanswer.php?mod=huzhu)
- [代码](https://github.com/LewisTian/Python/blob/master/fishC/jandan.py)
    - 此代码并没有加下载图片的函数。因为我之前试过爬微博图片，与其自己写下载函数，倒不如把链接保存下来，全部扔到迅雷来下载，那样速度快多了
- 有时间改成多线程


### [爬取堆糖图片](https://github.com/LewisTian/Python/blob/master/duitang/picture.py)
- 有时间将爬取专辑的函数加上
<div align="center">
	<img src="https://i.loli.net/2017/11/13/5a09631192f59.png" alt="堆糖·古风" width="600">
</div>
