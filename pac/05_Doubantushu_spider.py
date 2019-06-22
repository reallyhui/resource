#-*- coding:utf-8 -*-
from gevent import monkey
monkey.patch_all()

from pac.base_spiderB import BaseSpiderB
from pac.utils import is_file_exist,extra_first
from lxml import etree
import json,time,gevent

class Maoyan(BaseSpiderB):
    def __init__(self,ua_type):
        super().__init__(ua_type)
        self.start_urls = [f"https://book.douban.com/top250?start={i}" for i in range(0,226,25)]
        is_file_exist("doubantushu.json")
    def get_data(self,resp):
        if not resp:
            # print(f'请求[{resp.url}],响应为空，不做解析')
            return
        html = etree.HTML(resp.content.decode())
        tables = html.xpath('//div/table')

        # print(len(dds))
        for table in tables[1:]:
            title = table.xpath("./tr/td[2]/div/a/text()")
            detail_url = table.xpath("./tr/td[2]/div/a/@href")
            info = table.xpath("./tr/td[2]/p/text()")
            score = table.xpath("./tr/td[2]/div[2]/span[2]/text()")
            desc = table.xpath('./tr/td[2]/p[2]/text()')
            item = {
                "title": extra_first(title),
                "detail_url": extra_first(detail_url),
                "info": extra_first(info),
                "score": extra_first(score),
                "desc": extra_first(desc),
            }
            yield item
    def save_data(self,data):
        with open("doubantushu.json","a",encoding="utf-8") as f:
            f.write(json.dumps(data,ensure_ascii=False)+",\n")
    def woker(self,urls):
        for url in urls:
            resp = self.parse_url(url)
            for data in self.get_data(resp):
                self.save_data(data)

    def run(self, **kwargs):
        start = time.time()
        gevent.joinall([gevent.spawn(
            self.woker,
            self.start_urls[i:i + 3]
        ) for i in range(0, len(self.start_urls), 3)])
        end = time.time()
        print(f"协程耗时: {round(end - start, 2)}s")
if __name__ == '__main__':
    spider = Maoyan('PC')
    spider.run(debug=True)
    # spider.run()