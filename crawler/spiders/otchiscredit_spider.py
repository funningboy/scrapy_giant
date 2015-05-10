# -*- coding: utf-8 -*-

import re
import json

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import OtcHisCreditItem

__all__ = ['OtcHisCreditSpider']

# http://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal.php?l=zh-tw
# json stream
# http://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal_result.php?l=zh-tw
# 融資 融券

class OtcHisCreditSpider(CrawlSpider):
    name = 'otchiscredit'
    allowed_domains = ['http://www.tpex.org.tw']
    download_delay = 2
    _headers = [
        (u'前日餘額',  u'preremain'),
        (u'賣出', u'sellvolume'),
        (u'買進', u'buyvolume'),
#        (u'現券'|u'現償', u'daytrade'),
        (u'今日餘額', u'curremain'),
        (u'限額', u'limit')
    ]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcHisCreditSpider, self).__init__()

    def start_requests(self):
        URLS = [
            'http://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal_result.php'
        ]
        for i, URL in enumerate(URLS):
            item = OtcHisCreditItem()
            item['data'] = []
            request = Request(
                URL,
                meta={
                    'item': item,
                    'cookiejar': i,
                    'index': i
                },
                callback=self.parse,
                dont_filter=True)
            yield request

    def parse(self, response):
        """ json stram """
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        item = response.meta['item']
        index = response.meta['index']
        item['data'] = []
        print response.body
        item = json.load(response.body, encoding='utf-8')
        print item

