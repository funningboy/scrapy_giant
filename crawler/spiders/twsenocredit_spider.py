# -*- coding: utf-8 -*-

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log

# http://www.twse.com.tw/ch/trading/exchange/BFI84U/BFI84U.php

__all__ = ['TwseNoCreditSpider']

class TwseNoCreditSpider(CrawlSpider):
    name = 'twsenocredit'
    allowed_domains = ['http://twse.com.tw']
    download_delay = 2
    _hearders = [
        (u'股票代號', u'stockid'),
        (u'股票名稱', u'stocknm'),
        (u'停券起日(最後回補日)', u'nocredit_starttime'),
        (u'停券迄日', u'nocredit_endtime'),
        (u'原因', u'reason')]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TwseHisStockSpider, self).__init__()
        URL = 'http://www.twse.com.tw/ch/trading/exchange/BFI84U/BFI84U.php'
        self.start_urls = [URL]

    def parse(self, response):
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        sel = Selector(response)
        elems = self.xpath('//tr')
        for elem in elems[3]:
            sub = {}
            its = elem.xpath('td/text()').extract()
            if len(its):
                continue
            its = [it.strip(string.whitespace).replace(',', '') for it in its]
            sub['stockid'] = it[0] if it[0] else None
            sub['stocknm'] = it[1] if it[1]else None
            yy, mm, dd = map(int, its[2].split('/')) if its[2] else [None]*3
            sub['nocredit_starttime'] = u"%s-%s-%s" % (1911+yy, mm, dd) if None not in [yy, mm, dd] else None
            yy, mm, dd = its[2].split('/') if its[3] else [None]*3
            sub['nocredit_endtime'] = u"%s-%s-%s" %(1911+yy, mm, dd) if None not in [yy, mm, dd] else None
            item['data'].append(sub)
        log.msg("item[0] %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item
