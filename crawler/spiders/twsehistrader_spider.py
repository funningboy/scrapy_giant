# -*- coding: utf-8 -*-

import re
import string

import scrapy
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import TwseHisTraderItem

from handler.iddb_handler import TwseIdDBHandler

__all__ = ['TwseHisTraderSpider']

class TwseHisTraderSpider(CrawlSpider):
    name = 'twsehistrader'
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
        super(TwseHisTraderSpider, self).__init__()

    def start_requests(self):
        kwargs = {
            'debug': self.settings.getbool('GIANT_DEBUG'),
            'limit': self.settings.getint('GIANT_LIMIT'),
            'opt': 'twse'
        }
        requests = []
        for stockid in TwseIdDBHandler().stock.get_ids(**kwargs):
            URL = 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx'
            request = Request(
                URL,
                callback=self.parse,
                dont_filter=True)
            item = TwseHisTraderItem()
            item['stockid'] = stockid
            request.meta['item'] = item
            requests.append(request)
        return requests

    def parse(self, response):
        """ override level 0 """
        item = response.meta['item']
        sel = Selector(response)
        # get asp cookie contents for sumbit form
        contents = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': sel.xpath('.//input[@id="__VIEWSTATE"]/@value').extract()[0],
            '__EVENTVALIDATION': sel.xpath('.//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
            'HiddenField_spDate': '',
            'HiddenField_page': 'PAGE_BS',
            'txtTASKNO': item['stockid'],
            'hidTASKNO': '',
            'btnOK': u'查詢'
        }
        # register next response handler after sumbit form
        request = FormRequest.from_response(
            response,
            formdata=contents,
            callback=self.parse_after_form_submit,
            dont_filter=True)
        request.meta['item'] = item
        yield request

    def parse_after_form_submit(self, response):
        """ level 1 """
        item = response.meta['item']
        sel = Selector(response)
        try:
            pages = sel.xpath('.//span[@id="sp_ListCount"]/text()').extract()[0]
        except:
            log.msg("fetch %s fail" % (item['stockid']), log.INFO)
            return
        URL = (
            'http://bsr.twse.com.tw/bshtm/bsContent.aspx?' +
            'StartNumber=%(stock)s&FocusIndex=All_%(pages)s&flg_Print=1') % {
                'stock': item['stockid'],
                'pages': pages
        }
        # register next response handler after page was found
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
        sel = Selector(response)
         # populate content
        item['traderlist'] = []
        item['url'] = response.url
        item['date'] = sel.xpath('.//td[@id="receive_date"]/text()').extract()[0].strip(string.whitespace).replace(',', '').replace('/', '-')
        elem = sel.xpath('.//td[@id="stock_id"]/text()').extract()[0].strip(string.whitespace).replace(',', '')
        m = re.search(r'([0-9a-zA-Z]+)(\W+)', elem.replace(u' ', u''))
        item['stockid'] = m.group(1) if m else None
        item['stocknm'] = m.group(2) if m else None
        item['open'] = sel.xpath('.//td[@id="open_price"]/text()').extract()[0].strip(string.whitespace).replace(',', '')
        item['high'] = sel.xpath('.//td[@id="high_price"]/text()').extract()[0].strip(string.whitespace).replace(',', '')
        item['low'] = sel.xpath('.//td[@id="low_price"]/text()').extract()[0].strip(string.whitespace).replace(',', '')
        item['close'] = sel.xpath('.//td[@id="last_price"]/text()').extract()[0].strip(string.whitespace).replace(',', '')
        item['volume'] = sel.xpath('.//td[@id="trade_qty"]/text()').extract()[0].strip(string.whitespace).replace(',', '')
        # populate traderlist content
        elems = sel.xpath('.//tr[re:test(@class, "column_value_price_[0-9]{1,2}")]')
        for elem in elems:
            sub = {}
            nwelem = [it.strip(string.whitespace).replace(',', '') for it in elem.xpath('.//td/text()').extract()]
            m = re.search(r'([0-9a-zA-Z]+)(\W+)?', nwelem[1].replace(u' ', u'').replace(u'\u3000', u''))
            sub.update({
                'index': nwelem[0] if nwelem[0] else -1,
                'traderid': m.group(1) if m else None,
                'tradernm': m.group(2) if m else None,
                'price': nwelem[2] if nwelem[2] else 0,
                'buyvolume': nwelem[3] if nwelem[3] else 0,
                'sellvolume': nwelem[4] if nwelem[4] else 0
            })
            item['traderlist'].append(sub)
        log.msg("fetch %s pass" % (item['stockid']), log.INFO)
        log.msg("item[0] %s ..." % (item['traderlist'][0]), level=log.DEBUG)
        yield item
