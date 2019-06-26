# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import SunItem


class TtsunSpider(CrawlSpider):
    name = 'ttsun'
    # 允许爬取的域名，除了下面的start_urls以外
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4']

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), LinkExtractor:链接提取器
        #  callback='parse_item',  指定解析函数
        # follow=True),     follow指明是否需要对链接提取器提取到的链接响应再做过滤

        #对于列表页的url,不需要做解析，仅需跟进过滤提取详情页的url
        Rule(LinkExtractor(allow=r'http://wz.sun0769.com/index.php/question/report?page=\d+'), follow=True),
        #详情页url
        Rule(LinkExtractor(allow=r'http://wz.sun0769.com/html/question/\d+/\d+.shtml'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        print(55555)
        i = {}
        item = SunItem()

        #根据详情页面爬取
        item['number'] =response.xpath('//tr/td[2]/span[2]/text()').extract_first().split(':')[-1].strip()
        item['title'] =response.xpath('/html/head/title/text()').extract_first().split('_')[0]
        item["detail_url"] = response.url

        #有些内容有图片解析规则则不同

        # img = response.xpath(
        #     context_xpath_
        # )

        img = response.xpath('//td[@class="txt16_3"]/div/img')
        if img:
            text = response.xpath('//div[@class="contentext"]/text()').extract()
        else:
            text = response.xpath('//td[@class="txt16_3"]/text()').extract()
            item["context"] = "".join([x.strip() for x in text if not x.isspace() and x])
            print(item)
            yield item
