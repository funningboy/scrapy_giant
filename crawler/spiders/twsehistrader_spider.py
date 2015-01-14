# -*- coding: utf-8 -*-
# http://fanli7.net/a/bianchengyuyan/C__/20131106/440079.html

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
from scrapy.http.cookies import CookieJar
from scrapy import log
from crawler.items import TwseHisTraderItem
from crawler.spiders.twsehistrader_captcha import TwseHisTraderCaptcha0

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
    content = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '',
        '__EVENTVALIDATION': '',
        'RadioButton_Normal': 'RadioButton_Normal',
        'TextBox_Stkno': '',
        'CaptchaControl1': '',
        'btnOK': u'查詢'
    }

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
        URL = 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx'
        for stockid in TwseIdDBHandler().stock.get_ids(**kwargs):
            item = TwseHisTraderItem()
            item['stockid'] = stockid
            self.content.update({'TextBox_Stkno': stockid})
            request = Request(
                URL,
                meta={
                    'item': item,
                    'content': self.content
                },
                callback=self.parse,
                dont_filter=True)
            requests.append(request)
        return requests

    def parse(self, response):
        # find captcha path
        sel = Selector(response)
        url = sel.xpath('.//td/div/div/img/@src').extract()[0]
        URL = 'http://bsr.twse.com.tw/bshtm/' + url
        # update content
        response.meta['content'].update({
            '__VIEWSTATE': sel.xpath('.//input[@id="__VIEWSTATE"]/@value').extract()[0],
            '__EVENTVALIDATION': sel.xpath('.//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
        })
        request = Request(
            URL,
            meta={
                'item': response.meta['item'],
                'content': response.meta['content']
            },
            callback=self.parse_after_captcha_find,
            dont_filter=True)
        yield request

    def parse_after_captcha_find(self, response):
        # use captcha alg
        arr = np.asarray(bytearray(response.body), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        text = TwseHisTraderCaptcha0(False).run(img)
        # fake for debug only
        #text = raw_input('test:')
        #print text
        response.meta['content'].update({
            'CaptchaControl1': text
        })
        # register next response handler after sumbit form
        URL = 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx'
        request = FormRequest(
            URL,
            meta={
                'item': response.meta['item'],
                'content': response.meta['content']
            },
            formdata=response.meta['content'],
            callback=self.parse_after_form_submit,
            dont_filter=True)
        yield request

    def parse_after_form_submit(self, response):
        sel = Selector(response)
        find = sel.xpath('.//a[@id="HyperLink_DownloadCSV"]/@href')
        if find:
            # register next response handler after csv was found
            cookieJar = response.meta.setdefault('cookie_jar', CookieJar())
            cookieJar.extract_cookies(response, response.request)
            URL = 'http://bsr.twse.com.tw/bshtm/bsContent.aspx?v=t'
            request = Request(
                URL,
                meta = {
                    'dont_merge_cookies': True,
                    'cookie_jar': cookieJar,
                    'item': response.meta['item']
                },
                callback=self.parse_after_page_find,
                dont_filter=True)
            cookieJar.add_cookie_header(request)
            yield request
        else:
            err = sel.xpath('//*[@id="Label_ErrorMsg"]/font/text()').extract()[0]
            if err == u'驗證碼錯誤!':
                URL = 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx'
                # iter loop until csv was found
                request = Request(
                    URL,
                    meta={
                        'item': response.meta['item'],
                        'content': response.meta['content']
                    },
                    callback=self.parse,
                    dont_filter=True)
                yield request
            else:
                item = response.meta['item']
                log.msg("fetch %s null" % (item['stockid']), level=log.INFO)

    def parse_after_page_find(self, response):
        item = response.meta['item']
        sel = Selector(response)
        date = sel.xpath('//*[@id="receive_date"]/text()').extract()[0]
        yy, mm, dd = date.split('/')
        item['date'] = "%s-%s-%s" % (yy, mm, dd)
        stockdd = sel.xpath('//*[@id="stock_id"]/text()').extract()[0]
        item['stockid'], item['stocknm'] = stockdd.split()
        URL = 'http://bsr.twse.com.tw/bshtm/bsContent.aspx'
        request = Request(
           URL,
           meta = {
               'dont_merge_cookies': True,
               'cookie_jar': response.meta['cookie_jar'],
               'item': item
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
        # populate top content
        item['url'] = response.url
        item['date'] = item['date']
        item['stockid'], item['stocknm'] = item['stockid'], ""
        item['open'] = 0
        item['high'] = 0
        item['low'] = 0
        item['close'] = 0
        item['volume'] = 0
        # use as pandas frame to dict
        #try:
        frame = pd.read_csv(
            StringIO(response.body), delimiter=',',
            na_values=['--'], header=None, skiprows=[0, 1, 2], encoding=None, dtype=np.object)
        #except:
        #    log.msg("fetch %s fail" %(item['stockid']), log.INFO)
        #    return
        # divided left right frames
        fm0, fm1 = frame.ix[:, 0:5], frame.ix[:, 6:]
        for fm in [fm0, fm1]:
            for elem in fm.dropna().T.to_dict().values():
                nwelem = [str(elem[it]).strip(string.whitespace).replace(',', '') for it in sorted(elem.keys())]
                sub = {}
                m = re.search(r'([0-9a-zA-Z]+)(\W+)?', nwelem[1].decode('cp950').replace(u'\u3000', u'').replace(u' ', u''))
                sub.update({
                    'index': nwelem[0] if nwelem[0] else -1,
                    'traderid': m.group(1) if m and m.group(1) else None,
                    'tradernm': m.group(2) if m and m.group(2) else "",
                    'price': nwelem[2] if nwelem[2] else 0,
                    'buyvolume': nwelem[3] if nwelem[3] else 0,
                    'sellvolume': nwelem[4] if nwelem[4] else 0
                })
                item['traderlist'].append(sub)
        log.msg("fetch %s pass" %(item['stockid']), log.INFO)
        log.msg("item[0] %s ..." % (item['traderlist'][0]), level=log.DEBUG)
        yield item
