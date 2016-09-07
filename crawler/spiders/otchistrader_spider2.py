# -*- coding: utf-8 -*-
 # -*- coding: utf-8 -*-
# http://www.wantgoo.com/stock/agentdata.aspx?StockNo=2330
import re
import string
import json

from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import OtcHisTraderItem

from handler.iddb_handler import OtcIdDBHandler


__all__ = ['OtcHisTraderSpider2']

class OtcHisTraderSpider2(CrawlSpider):
    name = 'otchistrader2'
    allowed_domains = ['http://www.wantgoo.com']
    download_delay = 6
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
        super(OtcHisTraderSpider2, self).__init__()
        kwargs = {
            'debug': crawler.settings.getbool('GIANT_DEBUG'),
            'limit': crawler.settings.getint('GIANT_LIMIT'),
#            'slice': crawler.settings.getint('GIANT_SLICE'),
            'opt': 'otc'
        }
        self._id = OtcIdDBHandler(**kwargs)

    def start_requests(self):
        for i,stockid in enumerate(self._id.stock.get_ids()):
            if self._id.stock.is_warrant(stockid):
                continue
            item = OtcHisTraderItem()
            item.update({
                'stockid': stockid,
                'count': 0
            })
            URL = (
                'http://www.wantgoo.com/stock/AgentData.aspx?' +
                'stockno=%(stockid)s' ) % {
                    'stockid': stockid
            }
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
        """
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
        sel = Selector(response)
        item = response.meta['item']
        item['traderlist'] = []
        item['url'] = response.url
        date = sel.xpath('.//*[@id="txtDaysDefine_s"]/@value').extract()[0]
        item['date'] = u"%s-%s-%s" % (date[0:4], date[5:7], date[8:10])
        item['stockid'], item['stocknm'] = item['stockid'], ''
        item['open'] = u'0'
        item['high'] = u'0'
        item['low'] = u'0'
        item['close'] = u'0'
        item['volume'] = u'0'
        URL = 'http://www.wantgoo.com/Stock/aStock/AgentStat_Ajax'
        request = Request(
            URL,
            meta={
                'item': item,
                'StockNo': item['stockid'],
                'Types': '3.5',
                'Rows': '50'
            },
            callback=self.parse_after_form_submit,
            dont_filter=True)
        yield request
        
    def parse_after_form_submit(self, response):
        item = response.meta['item']
        listjson = json.loads(response.body, encoding='utf8')
        retvals = listjson['returnValues']
        elems = json.loads(retvals, encoding='utf8')
        for elem in elems:
            if u'券商名稱' in elem:
                tradernm = elem[u'券商名稱'].replace('-', '').replace(u' ', u'')
                traderid = self._id.trader.get_id(tradernm)
                price = elem[u'均價'] 
                buyvolume = elem[u'買量']
                sellvolume = elem[u'賣量']
            elif u'券商名稱2' in elem: 
                tradernm = elem[u'券商名稱2'].replace('-', '').replace(u' ', u'')
                traderid = self._id.trader.get_id(tradernm)
                price = elem[u'均價2'] 
                buyvolume = elem[u'買量2']
                sellvolume = elem[u'賣量2']

            if not traderid:
                log.msg("%s not found at trader list" %(tradernm), log.INFO)
                continue
            sub = {
                'index': u'0',
                'traderid': u"%s" %(traderid),
                'tradernm': tradernm,
                'price':  u"%.2f" % (float(price)) if price else u'0',
                'buyvolume': u"%d" % (float(buyvolume)*1000) if buyvolume else u'0',
                'sellvolume': u"%d" % (float(sellvolume)*1000) if sellvolume else u'0'
            }
            item['traderlist'].append(sub)
        log.msg("fetch %s pass at %d times" %(item['stockid'], item['count']), log.INFO)
        log.msg("item[0] %s ..." % (item['traderlist'][0]), level=log.DEBUG)
        yield item
