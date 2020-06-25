# -*- coding: utf-8 -*-
import scrapy
import json
import time

name_list = ['Rsvr', 'River', 'HydroInfo']


class HydroSearchSpider(scrapy.Spider):
    def __init__(self):
        self.num = 0
        self.f = open(r'logininfo.txt', 'w')

    name = 'hydro_search'  # 爬虫的名字，唯一标识符
    allowed_domains = ['xxfb.mwr.cn/hydroSearch/greatRsvr']
    start_urls = ['http://xxfb.mwr.cn/hydroSearch/greatRsvr',
                  'http://xxfb.mwr.cn/hydroSearch/greatRiver',
                  'http://xxfb.mwr.cn/hydroSearch/pointHydroInfo']  # 可传递多个

    def parse(self, response):
        time.sleep(8)
        try:
            res_j = json.loads(response.text)
            res_j['name'] = name_list[self.num]
            item = res_j
            yield item
            self.num += 1
            self.f.write("\t"+"登录成功")
            if self.num == 3:
                self.f.close()
        except :
            self.f.write("\n" + "发生异常")
