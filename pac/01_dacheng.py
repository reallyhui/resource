# -*- coding: utf8 -*-
from pac.base_spiderB import BaseSpiderB
from lxml import etree
from pac.utils import extra_first,is_file_exist
import json
import time
from gevent import monkey
monkey.patch_socket()
import gevent


class DachengSpider(BaseSpiderB):
    '''大成律师事务所爬虫'''
    def __init__(self,ua_type):
        super().__init__(ua_type)
        self.start_urls=[f'http://www.dachenglaw.com/cn/professionals?currentPageNo={i}&'.format(str(i)) for i in range(1,95)]
        is_file_exist('dacheng.json')
    def get_data(self,resp):
        '''取：解析数据'''
        '''{"name": "??", 
        "detail_url":"http://www.dachenglaw.com/cn/professionals/qi.ao.html",
         "email": "qi.ao@dentons.cn",
          "position":"?????", 
          "location": "??"}'''
        if not resp:
            # print(f"请求[{resp.url}],响应为空，不做解析")
            return
        html = etree.HTML(resp.content.decode())
        trs=html.xpath('//tbody/tr')
        items=[]
        for tr in trs:
            name=tr.xpath('./td[1]/a/text()')
            detail_url='http://www.dachenglaw.com'+extra_first(tr.xpath('./td[1]/a/@href'))
            email=tr.xpath('./td[2]/text()')
            position=tr.xpath('./td[3]/text()')
            location=tr.xpath('./td[4]/text()')

            ''''''
            #print(name,detail_url,email,position,location)
            item = {"name": extra_first(name),
                    "detail_url":detail_url,
                    "email": extra_first(email),
                    "position":extra_first(position),
                    "location": ''.join(extra_first(location).split())}
            yield item

    def save_data(self,data):
        '''存'''

        with open("dacheng.json","a",encoding="utf8") as f:
            # json.dump(data,f,ensure_ascii=False,indent=2)  #indent：缩进两个空格
            f.write(json.dumps(data,ensure_ascii=False)+",\n")
    # def run(self,**kwargs):
    #     start=time.time()
    #     super().run(**kwargs)
    #     end=time.time()
    #     print(f'单进程耗时：{round(end-start,2)}s')

    def worker(self,urls):
        for url in urls:
            resp = self.parse_url(url)
            for data in self.get_data(resp):
                self.save_data(data)

    def run(self, **kwargs):
        start = time.time()
        gevent.joinall([
            gevent.spawn(
                self.worker,
                self.start_urls[i:i + 10]
            ) for i in range(0, len(self.start_urls), 10)])
        end = time.time()
        print(f"协程耗时: {round(end - start, 2)}s")


if __name__ == '__main__':
    '''测试用例'''
    spider= DachengSpider("PC")
    # spider.run(debug=True)
    spider.run()