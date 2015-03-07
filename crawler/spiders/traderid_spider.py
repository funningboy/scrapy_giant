# -*- coding: utf-8 -*-

import re
import string

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from crawler.items import TraderIdItem

__all__ = ['TraderIdSpider']

class TraderIdSpider(CrawlSpider):
    name = 'traderid'
    allowed_domains = ['http://www.twse.com.tw']
    download_delay = 0.5

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TraderIdSpider, self).__init__()
        URL = 'http://www.twse.com.tw/ch/products/broker_service/broker2_list.php'
        self.start_urls = [URL]

    def parse(self, response):
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        sel = Selector(response)
        item = TraderIdItem()
        item['data'] = []
        elems = sel.xapth('.//*[@id="contentblock"]//tbody/basictxt')
        for elem in elems:
            sub = {}
            sub['traderid'] = elem.xpath('td[0]/text()').extract()
            sub['tradernm'] = elem.xpath('td[1]/a/text()').extract()
            item['data'].append(sub)
        log.msg("item[0] %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item
