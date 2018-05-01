# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.item import Item
import pymongo
from scrapy.pipelines.files import FilesPipeline
from os.path import basename

# 共享变量，定义系列型数据才能共享
topic = {'path':''}



class JdspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    @classmethod
    def from_crawler(cls,crawler):
        cls.DB_URI = crawler.settings.get('MONGGO_DB_URI','mongodb://localhost:27017')
        cls.DB_NAME = crawler.settings.get('DB_NAME','Data')
        return cls()

    def open_spider(self,spider):
        self.client =pymongo.MongoClient(self.DB_URI)
        self.db = self.client[self.DB_NAME]

    def process_item(self,item,spider):
        collection = self.db[topic['path']]
        data = dict(item) if isinstance(item,Item) else item
        collection.insert_one(data)

    def close_spider(self,spider):
        self.client.close()


class myImagePipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        return topic['path']+'/%s' % basename(request.url)

