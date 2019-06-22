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
        self.start_urls = [f"https://movie.douban.com/top250?start={i}&filter=" for i in range(0,250,25)]
        is_file_exist("douban.json")
    def get_data(self,resp):
        if not resp:
            # print(f'请求[{resp.url}],响应为空，不做解析')
            return
        html = etree.HTML(resp.content.decode())
        lis = html.xpath('//ol/li')
        # print(len(lis))
        for li in lis:
            id = li.xpath("./div/div/em/text()")
            title = li.xpath("./div/div/a/img/@alt")
            detail_url = li.xpath("./div/div/a/@href")
            content = li.xpath("./div/div[2]/div[2]/p/text()")
            score = li.xpath("./div/div[2]/div[2]/div/span[2]/text()")
            info = li.xpath('./div/div[2]/div[2]/p/span/text()')
            item = {
                "id": extra_first(id),
                "title":extra_first(title),
                "detail_url": extra_first(detail_url),
                "content": extra_first(content),
                "score": extra_first(score),
                "info": extra_first(info),
            }
            yield item
    def save_data(self,data):
        with open("douban.json","a",encoding="utf-8") as f:
            f.write(json.dumps(data,ensure_ascii=False)+",\n")

    # def run(self ,**kwargs):
    #     start = time.time()
    #     super().run(**kwargs)
    #     end = time.time()
    #     print(f"单进程耗时：{round(end-start,2)}s")

    def woker(self,urls):
        for url in urls:
            resp = self.parse_url(url)
            for data in self.get_data(resp):
                self.save_data(data)

    def run(self, **kwargs):
        start = time.time()
        gevent.joinall([gevent.spawn(
            self.woker,
            self.start_urls[i:i + 2]
        ) for i in range(0, len(self.start_urls), 2)])
        end = time.time()
        print(f"协程耗时: {round(end - start, 2)}s")
if __name__ == '__main__':
    spider = Maoyan('PC')
    spider.run(debug=True)