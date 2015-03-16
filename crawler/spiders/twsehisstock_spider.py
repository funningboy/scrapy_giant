# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np
from StringIO import StringIO
import string
from dateutil.relativedelta import relativedelta
from datetime import datetime

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import TwseHisStockItem

from handler.iddb_handler import TwseIdDBHandler

__all__ = ['TwseHisStockSpider']

class TwseHisStockSpider(CrawlSpider):
    name = 'twsehisstock'
    allowed_domains = ['http://www.twse.com.tw']
    download_delay = 0.5
    _headers = [
        (u'日期', u'date'),
        (u'成交股數', u'volume'),
        (u'成交金額', u'exhprice'),
        (u'開盤價', u'open'),
        (u'最高價', u'high'),
        (u'最低價', u'low'),
        (u'收盤價', u'close'),
        (u'漲跌價差', u'offset'),
        (u'成交筆數', u'exhvolume')]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TwseHisStockSpider, self).__init__()

    def start_requests(self):
        kwargs = {
            'debug': self.settings.getbool('GIANT_DEBUG'),
            'limit': self.settings.getint('GIANT_LIMIT'),
            'opt': 'twse'
        }
        requests = []
        for i,stockid in enumerate(TwseIdDBHandler().stock.get_ids(**kwargs)):
            for mon in range(2, -1, -1):
                timestamp = datetime.utcnow() - relativedelta(months=mon)
                if mon == 0:
                    if timestamp.day == 1 and timestamp.hour <= 14:
                        continue
                URL = (
                    'http://www.twse.com.tw/ch/trading/exchange/' +
                    'STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/' +
                    'Report%(year)d%(mon)02d/%(year)d%(mon)02d_F3_1_8_%(stock)s.php' +
                    '&type=csv') % {
                        'year': timestamp.year,
                        'mon': timestamp.month,
                        'stock': stockid
                }
                item = TwseHisStockItem()
                item.update({
                    'stockid': stockid,
                    'count': 0
                })
                request = Request(
                    URL,
                    meta= {
                        'item': item,
                        'cookiejar': i
                    },
                    callback=self.parse,
                    dont_filter=True)
                requests.append(request)
        return requests

    def parse(self, response):
        """
        data struct
        [
            {
                'date':
                'stockid':
                'oepn':
                'high':
                'low':
                'close':
                'volume':
            }, ...
        ]
        """
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        item = response.meta['item']
        item['url'] = response.url
        item['data'] = []
        # use as pandas frame to dict
        try:
            frame = pd.read_csv(
                StringIO(response.body), delimiter=',',
                na_values=['--'], header=None, skiprows=[0, 1], dtype=np.object).dropna()
            if frame.empty:
                log.msg("fetch %s empty" % (item['stockid']), log.INFO)
                return
        except:
            log.msg("fetch %s fail" % (item['stockid']), log.INFO)
            return
        for elems in frame.T.to_dict().values():
            nwelem = [str(it).strip(string.whitespace).replace(',', '') for it in elems.values()]
            sub = {}
            for indx, elem in enumerate(nwelem):
                if indx == 0:
                    yy, mm, dd = elem.split('/')
                    yy = int(yy) + 1911
                    sub[self._headers[indx][1]] = "%s-%s-%s" % (yy, mm, dd)
                    sub['stockid'] = item['stockid']
                else:
                    sub[self._headers[indx][1]] = elem.replace(',', '')
            item['data'].append(sub)
        log.msg("fetch %s pass at %d times" % (item['stockid'], item['count']), log.INFO)
        log.msg("item[0]: %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item
