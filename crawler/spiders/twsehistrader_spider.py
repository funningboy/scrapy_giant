# -*- coding: utf-8 -*-
# http://fanli7.net/a/bianchengyuyan/C__/20131106/440079.html
# https://github.com/scrapy/scrapy/blob/master/tests/test_downloadermiddleware_redirect.py
# only run for warrant
import re
import pandas as pd
import numpy as np
from StringIO import StringIO
import string
import cv2

from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import TwseHisTraderItem
from crawler.spiders.twsehistrader_captcha import TwseHisTraderCaptcha0, TwseHisTraderCaptcha1

from handler.iddb_handler import TwseIdDBHandler

__all__ = ['TwseHisTraderSpider']

class TwseHisTraderSpider(CrawlSpider):
    name = 'twsehistrader'
    allowed_domains = ['http://bsr.twse.com.tw']
    download_delay = 2
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
        kwargs = {
            'debug': crawler.settings.getbool('GIANT_DEBUG'),
            'limit': crawler.settings.getint('GIANT_LIMIT'),
#            'slice': crawler.settings.getint('GIANT_SLICE'),
            'opt': 'twse'
        }
        self._id = TwseIdDBHandler(**kwargs)

    def start_requests(self):
        URL = 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx'
        for i,stockid in enumerate(self._id.stock.get_ids()):
#            if not idhandler.stock.is_warrant(stockid):
#                continue
            item = TwseHisTraderItem()
            item.update({
                'stockid': stockid,
                'count': 0
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
        # find captcha url path
        item = response.meta['item']
        sel = Selector(response)
        URL = 'http://bsr.twse.com.tw/bshtm/' + sel.xpath('.//td/div/div/img/@src').extract()[0]
        content = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': sel.xpath('.//input[@id="__VIEWSTATE"]/@value').extract()[0],
            '__EVENTVALIDATION': sel.xpath('.//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
            'RadioButton_Normal': 'RadioButton_Normal',
            'TextBox_Stkno': item['stockid'],
            'CaptchaControl1': '',
            'btnOK': u'查詢'
        }
        request = Request(
            URL,
            meta={
                'item': item,
                'content': content,
                'cookiejar': response.meta['cookiejar']
            },
            callback=self.parse_after_captcha_find,
            dont_filter=True)
        yield request

    def parse_after_captcha_find(self, response):
        # use captcha alg as text decode
        item, content = response.meta['item'], response.meta['content']
        arr = np.asarray(bytearray(response.body), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        text = TwseHisTraderCaptcha0(False).run(img)
        #text = raw_input('test:')
        content.update({
            'CaptchaControl1': text
        })
        URL = 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx'
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
        item = response.meta['item']
        sel = Selector(response)
        find = sel.xpath('.//a[@id="HyperLink_DownloadCSV"]/@href')
        if find:
            URL = 'http://bsr.twse.com.tw/bshtm/bsContent.aspx?v=t'
            request = Request(
                URL,
                meta = {
                    'item': item,
                    'cookiejar': response.meta['cookiejar']
                },
                callback=self.parse_after_page_find,
                dont_filter=True)
            yield request
        else:
            err = sel.xpath('.//*[@id="Label_ErrorMsg"]/font/text()').extract()[0]
            if re.match(ur'.*驗證碼.*', err, re.UNICODE):
                URL = 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx'
                item['count']+=1
                request = Request(
                    URL,
                    meta={
                        'item': item,
                        'cookiejar': response.meta['cookiejar']
                    },
                    callback=self.parse,
                    dont_filter=True)
                yield request
            else:
                log.msg("fetch %s null %s" % (item['stockid'], err), level=log.INFO)

    def parse_after_page_find(self, response):
        item = response.meta['item']
        sel = Selector(response)
        date = sel.xpath('.//*[@id="receive_date"]/text()').extract()[0]
        yy, mm, dd = date.split('/')
        item['date'] = u"%s-%s-%s" % (yy, mm, dd)
        stockdd = sel.xpath('.//*[@id="stock_id"]/text()').extract()[0]
        item['stockid'], item['stocknm'] = stockdd.split()
        URL = 'http://bsr.twse.com.tw/bshtm/bsContent.aspx'
        request = Request(
           URL,
           meta = {
               'item': item,
                'cookiejar': response.meta['cookiejar']
           },
           callback=self.parse_after_csv_find,
           dont_filter=True)
        yield request

    def parse_after_csv_find(self, response):
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
        item = response.meta['item']
        item['traderlist'] = []
        item['url'] = response.url
        item['date'] = item['date']
        item['stockid'], item['stocknm'] = item['stockid'], None
        item['open'] = u'0'
        item['high'] = u'0'
        item['low'] = u'0'
        item['close'] = u'0'
        item['volume'] = u'0'
        # use as pandas frame to dict
        try:
            frame = pd.read_csv(
                StringIO(response.body), delimiter=',',
                na_values=['--'], header=None, skiprows=[0, 1, 2], encoding=None, dtype=np.object)
        except:
            log.msg("fetch %s fail" %(item['stockid']), log.INFO)
            return
        # divided left right frames
        fm0, fm1 = frame.ix[:, 0:5], frame.ix[:, 6:]
        for fm in [fm0, fm1]:
            for elem in fm.dropna().T.to_dict().values():
                nwelem = [str(elem[it]).strip(string.whitespace).replace(',', '') for it in sorted(elem.keys())]
                m = re.search(r'([0-9a-zA-Z]+)(\W+)?', nwelem[1].decode('cp950').replace(u'\u3000', u'').replace(u' ', u''))
                sub = {
                    'index': nwelem[0] if nwelem[0] else u'-1',
                    'traderid': m.group(1) if m and m.group(1) else None,
                    'tradernm': m.group(2) if m and m.group(2) else None,
                    'price': nwelem[2] if nwelem[2] else u'0',
                    'buyvolume': nwelem[3] if nwelem[3] else u'0',
                    'sellvolume': nwelem[4] if nwelem[4] else u'0'
                }
                item['traderlist'].append(sub)
        log.msg("fetch %s pass at %d times" %(item['stockid'], item['count']), log.INFO)
        log.msg("item[0] %s ..." % (item['traderlist'][0]), level=log.DEBUG)
        yield item
