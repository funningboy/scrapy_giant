# -*- coding: utf-8 -*-

import re
import string

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from crawler.items import OtcIdItem

# TWSE id : http://isin.twse.com.tw/isin/C_public.jsp?strMode=4
# ref https://github.com/samho5888/pyStockGravity/blob/master/src/StockIdDb.py

__all__ = ['OtcIDSpider']

class OtcIDSpider(CrawlSpider):
    name = 'otcid'
    allowed_domains = ['http://isin.twse.com.tw']

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcIDSpider, self).__init__()
        URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
        self.start_urls = [URL]

    def parse(self, response):
        """ override level 0 """
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        sel = Selector(response)
        item = OtcIdItem()
        item['data'] = []
        elems = sel.xpath('.//tr')
        for elem in elems[1:]:
            sub = {}
            its = elem.xpath('td/text()').extract()
            if len(its) <= 5:
                continue
            its = [it.strip(string.whitespace).replace(',', '') for it in its]
            m = re.search(r'([0-9a-zA-Z]+)(\W+)?', its[0].replace(u' ', u'').replace(u'\u3000', u''))
            sub['stockid'] = m.group(1) if m else None
            sub['stocknm'] = m.group(2) if m else None
            yy, mm, dd = its[2].split('/') if its[2] else [None]*3
            sub['onmarket'] = "%s-%s-%s" % (yy, mm, dd)
            sub['industry'] = its[4] if its[4] else None
            item['data'].append(sub)
        log.msg("item[0] %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item
