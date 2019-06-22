# -*- coding: utf8 -*-
from retrying import retry
import requests
from pac.utils import wait,UA_MAP

class BaseSpiderB(object):
    """爬虫基类"""
    def __init__(self,ua_type):
        """必要初始化"""
        self.start_urls = ["https://www.baidu.com"]
        self.headers = {
            "User-Agent": UA_MAP[ua_type]
        }

    #添加请求休眠装饰器，确定没有反爬时可以不用
    # @wait
    @retry(stop_max_attempt_number=3)
    def __parse_url(self,url):
        print(f'开始请求{[url]}')
        """发请求"""
        resp =  requests.get(
            url,
            headers=self.headers,
            timeout=3   #设置请求超时
        )
        assert resp.status_code == 200
        return resp

    def parse_url(self,url):
        """爬"""
        try:
            resp = self.__parse_url(url)
        except Exception as e:
            print(e)
            resp = None
        return resp

    def get_data(self,resp):
        """取"""
        raise NotImplementedError

    def save_data(self,data):
        """存"""
        raise NotImplementedError

    def run(self,**kwargs):
        """启动"""
        for url in self.start_urls:
            resp = self.parse_url(url)
            for data in self.get_data(resp):
                if kwargs.get("debug"):
                    return
                self.save_data(data)