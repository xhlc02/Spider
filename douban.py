#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:xhl time:2019\4\21 0021
# 第一章：爬虫豆瓣电影
import requests
from lxml import etree
# 1.将网站上的页面捉取下来
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Referer': 'https://movie.douban.com/'
}

url = 'https://movie.douban.com/cinema/nowplaying/guangzhou/'
response = requests.get(url=url, headers=headers)
#print(response.text)
# 保存到text变量里面
text = response.text
# 2.将捉取下来的页面进行提取
html =etree.HTML(text)
# 只获取到正在上映的
ul = html.xpath("//ul[@class='lists']")[0]
#print(etree.tostring(ul, encoding='utf-8').decode("utf-8"))
#拿到每一个lis
lis = ul.xpath("./li")
#定义一个列表
movies = []
#遍历每一个li
for li in lis:
    title = li.xpath("@data-title")[0]
    score = li.xpath("@data-score")[0]
    duration = li.xpath("@data-duration")[0]
    region = li.xpath("@data-region")[0]
    actors = li.xpath("@data-actors")[0]
    thumbnail = li.xpath(".//img/@src")[0]
    movie = {
        'title': title,
        'score': score,
        'duration': duration,
        'region': region,
        'actors': actors,
        'thumbnail': thumbnail
    }
    movies.append(movie)
print(movies)
