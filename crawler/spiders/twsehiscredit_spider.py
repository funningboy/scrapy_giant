# -*- coding: utf-8 -*-

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log


__all__ = ['TwseHisCreditSpider']
#
# 融券/融券 { 前日餘額, 賣出, 買進, 現券/現償, 今日餘額, 限額 }

# 融資: http://www.twse.com.tw/ch/trading/exchange/TWTA1U/TWTA1U.php
# 融券: http://www.twse.com.tw/ch/trading/exchange/TWT93U/TWT93U.php

class TwseHisCreditSpider(CrawlSpider):
    name = 'twsehiscredit'
    allowed_domains = ['http://twse.com.tw']
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
        super(TwseHisCreditSpider, self).__init__()

    def start_requests(self):
        URLS = [
            'http://www.twse.com.tw/ch/trading/exchange/TWTA1U/TWTA1U.php',
            'http://www.twse.com.tw/ch/trading/exchange/TWT93U/TWT93U.php'
        ]
        for i, URL in enumerate(URLS):
            item = TwseCreditItem()
            item['data'] = []
            request = Request(
                URL,
                meta={
                    'item': item,
                    'index': i
                },
                callback=self.parse,
                dont_filter=True)
            yield request

    def parse(self, response):
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        sel = Selector(response)
        item = response.meta['item']
        index = response.meta['index']
        try:
            frame = pf.frame
        except:
            log.msg
            return
        #self.xpath('.//*[@id="contentblock"]/td/table[2]/tbody/tr/td/table[2]/tbody/tr/td/div')
        elems = self.xpath('.//*[@id="tbl-containerx"]//tr')
        for elem in elems[1:]:
            its = elem.xpath('td/text()').extract()
            if len(its) <= 8:
                continue
            its = [it.strip(string.whitespace).replace(',', '') for it in its]
            sub = {k: its[i] for i, k in enumerate([
                    'stockid',
                    'stocknm',
                    'preremain',
                    'buyvolume',
                    'sellvolume',
                    'daytrade',
                    'curremain',
                    'limit'])}
            sub.update({
                'date': date,
                'type': 'finance' if index == 0 else 'bearish'
            })
            item['data'].append(sub)
        log.msg("item[0] %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item
