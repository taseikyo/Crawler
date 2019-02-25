#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-25 14:43:58
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os
import jieba
from wordcloud import WordCloud
from imageio import imread

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 设置中文字体
font_path = 'C:/Users/tian/Downloads/fonts/free/思源黑体/SourceHanSansCN-Bold.otf'

# stopword
stopword_path = os.path.join(BASE_DIR, 'stopwords.txt')

# 读入 stopword
with open(stopword_path, encoding='utf-8') as f_stop:
    f_stop_text = f_stop.read()
    f_stop_seg_list = f_stop_text.splitlines()

# 读入文本内容
text = open(os.path.join(BASE_DIR, 'bili-mad.txt'), encoding='utf-8').read()

# 中文分词
seg_list = jieba.cut(text, cut_all=False)

# 把文本中的stopword剃掉
my_word_list = []

for my_word in seg_list:
    if len(my_word.strip()) > 1 and not (my_word.strip() in f_stop_seg_list):
        my_word_list.append(my_word)

my_word_str = ' '.join(my_word_list)

# 生成词云
# wc = WordCloud(
#     font_path=font_path,
#     background_color="white",
#     random_state=1024,
#     width=1920,
#     height=1080,
# )

wc = WordCloud(
    background_color='white',
    mask=imread('bilibili.jpg'),
    font_path=font_path
)

wc.generate(my_word_str)

# 生成图片
wc.to_file('bili-mad.png')
