# -*- coding: utf-8 -*-
# @Time    : 2020/6/4 10:49
# @Author  : ding
# @File    : begin.py

from scrapy import cmdline


def main():
    cmdline.execute("scrapy crawl hydro_search".split())


if __name__ == '__main__':
    main()
