# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np
from StringIO import StringIO
import string

import scrapy
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import OtcHisTraderItem

from query.iddb_query import OtcIdDBQuery

__all__ = ['OtcHisTraderSpider']

class OtcHisTraderSpider(CrawlSpider):
    name = 'otchistrader'
    allowed_domains = ['http://bsr.twse.com.tw']
    _headers = [
        (u'序號', u'index'),
        (u'券商', u'traderid'),
        (u'價格', u'price'),
        (u'買進股數', u'buyvolume'),
        (u'賣出股數', u'sellvolume')
    ]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcHisTraderSpider, self).__init__()

    def start_requests(self):
        kwargs = {
            'debug': self.settings.getbool('GIANT_DEBUG'),
            'limit': self.settings.getint('GIANT_LIMIT')
        }
        requests = []
        for stockid in OtcIdDBQuery().get_stockids(**kwargs):
            URL = (
                'http://www.gretai.org.tw/web/stock/aftertrading/' +
                'broker_trading/brokerBS.php?l=zh-tw&stk_code=%(stock)s') % {
                    'stock': stockid
            }
            request = Request(
                URL,
                callback=self.parse,
                dont_filter=True)
            item = OtcHisTraderItem()
            item['stockid'] = stockid
            request.meta['item'] = item
            requests.append(request)
        return requests

    def parse(self, response):
        """ override level 0 """
        item = response.meta['item']
        sel = Selector(response)
        try:
            date = sel.xpath(".//input[@id='stk_date']/@value").extract()[0]
        except:
            log.msg("fetch %s fail" %(item['stockid']), log.INFO)
            return
        URL = (
            'http://www.gretai.org.tw/web/stock/aftertrading/' +
            'broker_trading/download_ALLCSV.php?' +
            'curstk=%(stock)s&stk_date=%(date)s') % {
            'stock': item['stockid'],
            'date': date
        }
        yy, mm, dd = date[:-4], date[-4:-2], date[-2:]
        item['date'] = "%s-%s-%s" % (int(yy) + 1911, mm, dd)
        request = Request(
            URL,
            callback=self.parse_after_page_find,
            dont_filter=True)
        request.meta['item'] = item
        yield request

    def parse_after_page_find(self, response):
        """ level 2
        data struct
        {
            'date':
            'stockid':
            'stocknm':
            'traderlist':
                [
                    {
                        'index':
                        'traderid':
                        'tradernm':
                        'price':
                        'buyvolume':
                        'sellvolume':
                    },
                    ...
                ].sort(buyvo)limit(30)
        }
        """
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        item = response.meta['item']
        item['traderlist'] = []
        # populate top content
        item['url'] = response.url
        item['date'] = item['date']
        item['stockid'], item['stocknm'] = item['stockid'], None
        item['open'] = 0
        item['high'] = 0
        item['low'] = 0
        item['close'] = 0
        item['volume'] = 0
        # use as pandas frame to dict
        try:
            frame = pd.read_csv(
                StringIO(response.body), delimiter=',',
                na_values=['--'], header=None, skiprows=[0, 1, 2], encoding=None, dtype=np.object)
            if frame.empty:
                log.msg("fetch %s empty" %(item['stockid']), log.INFO)
                return
        except:
            log.msg("fetch %s fail" %(item['stockid']), log.INFO)
            return
        # divided left right frames
        fm0, fm1 = frame.ix[:, 0:5], frame.ix[:, 6:]
        for fm in [fm0, fm1]:
            for elem in fm.T.to_dict().values():
                nwelem = [str(elem[it]).strip(string.whitespace).replace(',', '') for it in sorted(elem.keys())]
                sub = {}
                m = re.search(r'([0-9a-zA-Z]+)(\W+)?', nwelem[1].decode('cp950').replace(u'\u3000', u'').replace(u' ', u''))
                sub.update({
                    'index': nwelem[0] if nwelem[0] else -1,
                    'traderid': m.group(1) if m else None,
                    'tradernm': m.group(2) if m else None,
                    'price': nwelem[2] if nwelem[2] else 0,
                    'buyvolume': nwelem[3] if nwelem[3] else 0,
                    'sellvolume': nwelem[4] if nwelem[4] else 0
                })
                item['traderlist'].append(sub)
        log.msg("fetch %s pass" %(item['stockid']), log.INFO)
        log.msg("item[0] %s ..." % (item['traderlist'][0]), level=log.DEBUG)
        yield item
