# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class books(scrapy.Item):
    title = scrapy.Field() #书名
    detail = scrapy.Field() #简介
    price = scrapy.Field() # 价格
    author = scrapy.Field() #作者
    commitNum = scrapy.Field() # 评论数
    shopNum = scrapy.Field()  #出版社
    file_urls = scrapy.Field()
    # product = scrapy.Field()