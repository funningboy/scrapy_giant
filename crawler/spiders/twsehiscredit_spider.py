# -*- coding: utf-8 -*-

import re
import string

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import TwseHisCreditItem

__all__ = ['TwseHisCreditSpider']
#
# 融券/融券 { 前日餘額, 賣出, 買進, 現券/現償, 今日餘額, 限額 }

# 融資: http://www.twse.com.tw/ch/trading/exchange/TWTA1U/TWTA1U.php 單位: 交易單位
# 融券: http://www.twse.com.tw/ch/trading/exchange/TWT93U/TWT93U.php 單位: 股

class TwseHisCreditSpider(CrawlSpider):
    name = 'twsehiscredit'
    allowed_domains = ['http://twse.com.tw']
    download_delay = 2
    _headers = [
        (u'前日餘額',  u'preremain'),
        (u'賣出', u'sellvolume'),
        (u'買進', u'buyvolume'),
        (u'現券|現償', u'daytrade'),
        (u'今日餘額', u'curremain'),
        (u'限額', u'limit')
    ]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TwseHisCreditSpider, self).__init__()

    def start_requests(self):
        URLS = [
            'http://www.twse.com.tw/ch/trading/exchange/TWTA1U/TWTA1U.php',
            'http://www.twse.com.tw/ch/trading/exchange/TWT93U/TWT93U.php'
        ]
        for i, URL in enumerate(URLS):
            item = TwseHisCreditItem()
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
        """ html """
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        sel = Selector(response)
        item = response.meta['item']
        index = response.meta['index']
        item['url'] = response.url
        date = sel.xpath('///*[@id="date-field"]/@value').extract()[0]
        yy, mm, dd = map(int, date.split('/'))
        elems = sel.xpath('.//*[@id="main-content"]/table/tbody/tr')
        for elem in elems[:-1]:
            its = elem.xpath('./td/text()').extract()
            if len(its) < 8:
                continue
            its = [it.strip(string.whitespace).replace(',', '') for it in its]
            sub = {
                'date': "%s-%s-%s" %(yy+1911, mm, dd),
                'type': 'finance' if index == 0 else 'bearish',
                'stockid': its[0],
                'stocknm': its[1],
                'preremain': int(its[2]) if index == 0 else int(its[2]) // 1000,
                'buyvolume': int(its[3]) if index == 0 else int(its[4]) // 1000,
                'sellvolume': int(its[4]) if index == 0 else int(its[3]) // 1000,
                'daytrade': int(its[5]) if index == 0 else int(its[5]) // 1000,
                'curremain': int(its[6]) if index == 0 else int(its[6]) // 1000,
                'limit': int(its[7]) if index == 0 else int(its[7]) // 1000
            }
            item['data'].append(sub)
        log.msg("item[0] %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item

    def parse_after_csv_find(self, response):
        """ not utf-8 format...
        data struct
        [
            {
                'date':
            }, ...
        ]
        """
        pass
