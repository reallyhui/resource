# -*- coding: utf8 -*-
from pac.base_spiderB import BaseSpiderB
from lxml import etree
from pac.utils import is_file_exist,extra_first
import json
import time

class Maoyan(BaseSpiderB):
    '''猫眼电影'''
    def __init__(self,ua_type):
        super().__init__(ua_type)
        self.start_urls=[f'https://maoyan.com/board/4?offset={i}'.format(str(i)) for i in range(0,100,10)]
        is_file_exist('manyan.json')
    def get_data(self,resp):
        if not resp:
            return
        html=etree.HTML(resp.content.decode())
        trs = html.xpath('//dl/dd')
        items = []
        for i in trs:
            id = i.xpath('./i/text()')
            title=i.xpath('./a/@title')
            detail_url=i.xpath('./a/@href')
            actors=i.xpath('./div/div/div/p[2]/text()')
            releasetime=i.xpath('./div/div/div/p[3]/text()')
            score1=i.xpath('./div/div/div[2]/p/i[1]/text()')
            score2 = i.xpath('./div/div/div[2]/p/i[2]/text()')

            item = {"id": extra_first(id),
                    "detail_url": 'https://maoyan.com'+extra_first(detail_url),
                    "title":extra_first(title),
                    "actors": extra_first(actors),
                    "releasetime": extra_first(releasetime),
                    "score": extra_first(score1)+extra_first(score2)}
            yield item

    def save_data(self, data):
        '''存'''
        with open("maoyan.json", "a", encoding="utf8") as f:
            # json.dump(data,f,ensure_ascii=False,indent=2)  #indent：缩进两个空格
            f.write(json.dumps(data, ensure_ascii=False) + ",\n")
    def run(self,**kwargs):
        start=time.time()
        super().run(**kwargs)
        end=time.time()
        print(f'单进程耗时：{round(end-start,2)}s')


if __name__ == '__main__':
    '''测试用例'''
    spider= Maoyan("PC")
    # spider.run(debug=True)
    spider.run()
