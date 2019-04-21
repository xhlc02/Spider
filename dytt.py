#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:xhl time:2019\4\21 0021
# 第二章：电影天堂
from lxml import etree
import requests
# 全局变量地址
BASE_URL = 'http://www.ygdy8.net'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
#获取到一个页面的所有详情页面的地址
def getDetailUrl(url):
    response = requests.get(url=url, headers=HEADERS)
    # 网站需用gbk解码
    text = response.text
    html = etree.HTML(text)
    # 获取当前页面的每一个a标签的电影链接
    hrefs = html.xpath("//table[@class='tbspan']//a/@href")
    urls = map(lambda url: BASE_URL+url, hrefs)
    return urls
# 解析每一个详情页面
def parse(url):
    movie = {}
    response = requests.get(url=url, headers=HEADERS)
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    movie['titile'] = title
    zoom = html.xpath("//div[@id='Zoom']")[0]
    # 获取到当前电影的所有图片
    imgs = zoom.xpath(".//img/@src")
    # 获取到当前电影的海报
    cover = imgs[0]
    # 获取到当前电影的截图
    screenshot = imgs[1]
    movie['cover'] = cover
    movie['screenshot'] = screenshot
    # 获取到当前电影的所有信息
    infos = zoom.xpath(".//text()")

    def parse_info(info, rule):
        return info.replace(rule, "").strip

    for index, info in enumerate(infos):
        if info.startswith("◎年　　代"):
            # 将年代去掉，并且把年代的前后空格去掉
            info = parse_info(info, "◎年　　代")
            movie['year'] = info
        elif info.startswith("◎产　　地"):
            info = parse_info(info, "◎产　　地")
            movie['country'] = info
        elif info.startswith("◎类　　别"):
            info = parse_info(info, "◎类　　别")
            movie['type'] = info
        elif info.startswith("◎豆瓣评分"):
            info = parse_info(info, "豆瓣评分")
            movie['ping_fen'] = info
        elif info.startswith("◎片　　长"):
            info = parse_info(info, "◎片　　长")
            movie['duration'] = info
        elif info.startswith("◎导　　演"):
            info = parse_info(info, "◎导　　演")
            movie['director'] = info
        elif info.startswith("◎主　　演"):
            info = parse_info(info, "◎主　　演")
            actors = [info]
            for x in range(index+1, len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
            print(actors)
            movie["actors"] = actors
        elif info.startswith("◎简　　介"):
            info = parse_info(info, "◎简　　介")
            for x in range(index+1, len(infos)):
                profile = infos[x].strip()
                if profile.startswith("◎"):
                    break
            movie['profile'] = info
    download_url = html.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie["download"] = download_url
    return movie



#获取每个页面的url
def spider():
    base_url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'
    movies = []
    # 只获取前面5页的url
    for x in range(1, 6):
        # 拼接地址
        url = base_url.format(x)
        # 获取到当前页面的所有前往详情页面的地址
        detail_urls = getDetailUrl(url)
        for detail_url in detail_urls:
            movie = parse(detail_url)
            movies.append(movie)
            print(movies)
        return movies


if __name__ == '__main__':
    spider()

