#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from PIL import Image
from io import BytesIO
import time
import datetime
import os


def download_source(url_url, headers, cookies):
    """下载文件，返回一个内存中的图片，如果下载失败则返回bool值False"""
    raw_picture = requests.get(url=url_url, stream=False, headers=headers, verify=False, cookies=cookies)
    raw_picture = raw_picture.content
    if len(raw_picture) != 0:
        raw_picture = BytesIO(raw_picture)
        try:
            raw_picture = Image.open(raw_picture)
        except:
            print('网络错误')
            return False
        return raw_picture
    else:
        return False


cold_time = 0.01  # 全局下载冷却时间
url0 = input('输入封面地址：')

# 计算下载过程耗时
start_time = time.time()

url0 = url0.split('&')
# 准备链接头和链接尾
url_head = str(url0[0]) + '&' + str(url0[1]) + '&jid='
url_tail = '.jpg&zoom=0'

# 设置请求头以及cookie
headers0 = {'Host': 'jcft.lib.sjtu.edu.cn:83', 'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63',
            'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Referer': 'http://jcft.lib.sjtu.edu.cn:9088/', 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
cookies0 = {}  # 没错，通过这种复制图片链接而不是预览页面链接的方式，我们不用cookie就能下载
data = {}
# 初始化图片列表
images = list()

# 首先下载封面cov，然后直接添加到图片列表images中
print('开始下载封面')
images.append(download_source(url_head + '/cov001' + url_tail, headers0, cookies0))
# 再下载封面bok，然后直接添加到图片列表images中
images.append(download_source(url_head + '/bok001' + url_tail, headers0, cookies0))
# 再下载leg，然后直接添加到图片列表images中
images.append(download_source(url_head + '/leg001' + url_tail, headers0, cookies0))
print('封面下载完成')

# 使用一个while循环下载前言
i = 1
while True:
    url = url_head + "/fow" + f'{i:03d}' + url_tail
    img = download_source(url, headers0, cookies0)
    if isinstance(img, bool):
        print('前言下载完成')
        break
    else:
        images.append(img)
        print('前言下载中，完成第' + str(i) + '张前言的下载')
    i += 1
    time.sleep(cold_time)

# 使用一个while循环下载目录
i = 1
while True:
    url = url_head + "/!" + f'{i:05d}' + url_tail
    img = download_source(url, headers0, cookies0)
    if isinstance(img, bool):
        print('目录下载完成')
        break
    else:
        images.append(img)
        print('目录下载中，完成第' + str(i) + '张目录的下载')
    i += 1
    time.sleep(cold_time)

# 使用一个while循环下载正文
i = 1
while True:
    url = url_head + "/" + f'{i:06d}' + url_tail
    img = download_source(url, headers0, cookies0)
    if isinstance(img, bool):
        print('正文下载完成，开始将内存中的图片合成为PDF文档，保存在程序相同目录......')
        break
    else:
        images.append(img)
        print('正文下载中，完成第' + str(i) + '张正文的下载')
    i += 1
    time.sleep(cold_time)

# 保存PDF
img0 = images[0]
now = datetime.datetime.now()
if not os.path.exists('saved'):
    os.mkdir('saved')
pdf_name = '.\\saved\\图书下载' + now.strftime("%Y_%m_%d_%H_%M_%S") + '.pdf'
img0.save(pdf_name, "PDF", resolution=75.0, save_all=True, append_images=images[1:])
# 释放内存
images = 0

# 计算总过程耗时
end_time = time.time()
# 计算文件大小
file_size = os.path.getsize(pdf_name)/float(1024)/float(1024)
print('图书大小为：'+f'{file_size:.2f}'+'MB'+'，下载此本图书过程共耗时：' + f'{end_time - start_time:.2f}'+'s')
print('您要的文件已保存在:'+str(pdf_name))
input('按回车键退出...')
