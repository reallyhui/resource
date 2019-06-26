# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy.conf import settings
from pymongo import MongoClient

class TencentPipeline(object):

    def process_item(self, item, spider):
        return item

class MongoPipleline(object):
    def __init__(self):
        host= settings["MONGO_HOST"]
        port = settings["MONGO_PORT"]
        dbname = settings["MONGO_DBNAME"]
        colname = settings["MONGO_COLNAME"]

        # now_str=datetime.now().strftime("%m_%d_%H_%M")
        # colname += "_" + now_str

        self.handle = MongoClient(host,port)
        self.db = self.handle[dbname]
        self.col = self.db[colname]

    def process_item(self,item,spider):
        #1.将item对象转换为dict类型
        data = dict(item)
        #查询是否已经存在
        res = self.col.find_one({"_id":data["post_id"]})
        if not res:
            data["_id"] = data.pop("post_id")
            #若库中不存在，则存储数据
            self.col.insert(data)
        return item

    def close_spider(self,spider):
        '''资源关闭'''
        self.handle.close()

