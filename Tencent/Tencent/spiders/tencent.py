# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    start_urls = [f"https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex={i}&pageSize=200"
                  for i in range(1, 22)]
    detail_url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId={}"

    def parse(self, response):
        data_json=json.loads(response.text)
        for data in data_json["Data"]["Posts"]:
            item = TencentItem()
            item["name"]=data['RecruitPostName']
            item["post_id"] = data['PostId']
            item["publish_date"] = data['LastUpdateTime']
            item["category"] = data['CategoryName']
            item["duty"] = data['Responsibility']
            item["country"] = data['CountryName']
            item["location"] = data['LocationName']
            yield scrapy.Request(
                self.detail_url.format(item['post_id']),
                callback=self.perse_detail,
                meta=dict(item=item)
            )

    def perse_detail(self,response):
        '''详情页面'''
        item = response.meta["item"]
        data_json = json.loads(response.text)
        item['require'] = data_json['Data']['Requirement']
        # print(item['require'])
        yield item

