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
        self.start_urls = [f"https://www.kugou.com/yy/rank/home/{i}-8888.html" for i in range(1,24)]
        is_file_exist("kugou.json")
    def get_data(self,resp):
        if not resp:
            # print(f'请求[{resp.url}],响应为空，不做解析')
            return
        html = etree.HTML(resp.content.decode())
        lis = html.xpath('//div[@class="pc_temp_songlist "]/ul/li')
        # print(len(lis))
        for ll in lis:
            id = ll.xpath("./span[3]/text()")
            title = ll.xpath("./@title")
            detail_url = ll.xpath("./a/@href")
            time = ll.xpath("./span[4]/span/text()")
            item = {
                "id": extra_first(id),
                "title":extra_first(title),
                "detail_url": extra_first(detail_url),
                "time": extra_first(time),
            }
            yield item
    def save_data(self,data):
        with open("kugou.json","a",encoding="utf-8") as f:
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