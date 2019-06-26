# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()  # 岗位名称
    post_id = scrapy.Field()  # 岗位编号
    publish_date = scrapy.Field()  # 发布时间
    category = scrapy.Field()  # 工作分类
    duty = scrapy.Field()  # 岗位职责
    country = scrapy.Field()  # 国家
    location = scrapy.Field()  # 工作地点
    require = scrapy.Field()  # 工作要求
