# -*- coding: utf-8 -*-
 # -*- coding: utf-8 -*-
# http://www.wantgoo.com/stock/agentdata.aspx?StockNo=2330
import re
import string

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
        date = sel.xpath('.//*[@id="ctl00_ContentPlaceHolder1_DropDownList1"]/option[1]/text()').extract()[0]
        item['date'] = u"%s-%s-%s" % (date[0:4], date[4:6], date[6:8])
        item['stockid'], item['stocknm'] = item['stockid'], ''
        item['open'] = u'0'
        item['high'] = u'0'
        item['low'] = u'0'
        item['close'] = u'0'
        item['volume'] = u'0'
        elems = sel.xpath('.//table[@id="ctl00_ContentPlaceHolder1_GridView2"]//td/font/text()').extract()
        for i in xrange(0, len(elems)-20, 4):
            tradernm = elems[i].replace('-', '').replace(u'\u3000', u'').replace(u' ', u'')
            traderid = u"%s" %(OtcIdDBHandler().trader.get_id(tradernm))
            sub = {
                'index': u'0',
                'traderid': traderid,
                'tradernm': tradernm,
                'price': elems[i+3] if elems[i+3] else u'0',
                'buyvolume': u"%d" % (float(elems[i+1])*1000) if elems[i+1] else u'0',
                'sellvolume': u"%d" % (float(elems[i+2])*1000) if elems[i+2] else u'0'
            }
            item['traderlist'].append(sub)
        log.msg("fetch %s pass at %d times" %(item['stockid'], item['count']), log.INFO)
        log.msg("item[0] %s ..." % (item['traderlist'][0]), level=log.DEBUG)
        yield item

