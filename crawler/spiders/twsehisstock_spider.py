# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np
from StringIO import StringIO
import string
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
import traceback 

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import TwseHisStockItem

from handler.iddb_handler import TwseIdDBHandler

__all__ = ['TwseHisStockSpider']

"""
sync to 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAYMAIN.php'
"""


class TwseHisStockSpider(CrawlSpider):
    name = 'twsehisstock'
    allowed_domains = ['http://www.twse.com.tw']
    download_delay = 2
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
        kwargs = {
            'debug': crawler.settings.getbool('GIANT_DEBUG'),
            'limit': crawler.settings.getint('GIANT_LIMIT'),
            'opt': 'twse'
        }
        self._id = TwseIdDBHandler(**kwargs)

    def start_requests(self):
        URL = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAYMAIN.php'
        for i,stockid in enumerate(self._id.stock.get_ids()):
            if self._id.stock.is_warrant(stockid):
                continue
            for mon in range(2, -1, -1):
                timestamp = datetime.utcnow() - relativedelta(months=mon)
                if mon == 0:
                    if timestamp.day == 1 and timestamp.hour <= 14:
                        continue
                
                item = TwseHisStockItem()
                item.update({
                    'stockid': stockid,
                    'count': 0,
                    'year': "{0}".format(timestamp.year),
                    'month': "{0}".format(timestamp.month)
                })
                request = Request(
                    URL,
                    meta={
                        'item': item,
                        'cookiejar': i
                    },
                    callback=self.parse,
                    dont_filter=True)
                yield request

    def parse(self, response):
        URL = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAYMAIN.php'
        item = response.meta['item']
        sel = Selector(response)
        content = {
            'download': 'csv',
            'query_year': item['year'],
            'query_month': item['month'],
            'CO_ID': item['stockid'],
            'query-buttom': u'查詢'
        }
        request = FormRequest(
            URL,
            meta={
                'item': item,
                'cookiejar': response.meta['cookiejar']
            },
            formdata=content,
            callback=self.parse_after_form_submit,
            dont_filter=True)
        yield request

    def parse_after_form_submit(self, response):
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
                na_values=['--'], header=None, skiprows=[0, 1], dtype=np.object)
            # rm empty field
            del frame[9]
            if frame.empty:
                log.msg("fetch %s empty" % (item['stockid']), log.INFO)
                return
        except:
            print traceback.print_exc()
            log.msg("fetch %s fail" % (item['stockid']), log.INFO)
            return
        for elems in frame.T.to_dict().values():
            nwelem = [str(it).strip(string.whitespace).replace(',', '') for it in elems.values()]
            sub = {}
            for indx, elem in enumerate(nwelem):
                if indx == 0:
                    yy, mm, dd = map(int, elem.split('/'))
                    sub[self._headers[indx][1]] = "%s-%s-%s" % (1911+yy, mm, dd)
                    sub['stockid'] = item['stockid']
                else:
                    sub[self._headers[indx][1]] = elem.replace(',', '')
            item['data'].append(sub)
        log.msg("fetch %s pass at %d times" % (item['stockid'], item['count']), log.INFO)
        log.msg("item[0]: %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item