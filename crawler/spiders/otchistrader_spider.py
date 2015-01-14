# -*- coding: utf-8 -*-

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
from crawler.items import OtcHisTraderItem
from crawler.spiders.otchistrader_captcha import OtcHisTraderCaptcha1

from handler.iddb_handler import OtcIdDBHandler

__all__ = ['OtcHisTraderSpider']

class OtcHisTraderSpider(CrawlSpider):
    name = 'otchistrader'
    allowed_domains = ['http://www.gretai.org.tw']
    _headers = [
        (u'序號', u'index'),
        (u'券商', u'traderid'),
        (u'價格', u'price'),
        (u'買進股數', u'buyvolume'),
        (u'賣出股數', u'sellvolume')
    ]
    content = {
        'stk_code': '',
        'auth_num': ''
    }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcHisTraderSpider, self).__init__()

    def start_requests(self):
        kwargs = {
            'debug': self.settings.getbool('GIANT_DEBUG'),
            'limit': self.settings.getint('GIANT_LIMIT'),
            'opt': 'otc'
        }
        requests = []
        for stockid in OtcIdDBHandler().stock.get_ids(**kwargs):
            URL = (
                'http://www.gretai.org.tw/web/stock/aftertrading/' +
                'broker_trading/brokerBS.php?l=zh-tw&stk_code=%(stock)s') % {
                    'stock': stockid
            }
            item = OtcHisTraderItem()
            item['stockid'] = stockid
            self.content.update({'stk_code': stockid})
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
        URL = 'http://www.gretai.org.tw/web/inc/authnum.php'
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
        text = OtcHisTraderCaptcha1(False).run(img)
        # fake for debug only
        #text = raw_input('test:')
        #print text
        response.meta['content'].update({
            'auth_num': text
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
        find = sel.xpath('/html/body/center/div[3]/div[2]/div[4]/div[2]/div[2]/button[1]/text()')
        if find:
            # register next response handler after csv was found
            cookieJar = response.meta.setdefault('cookie_jar', CookieJar())
            cookieJar.extract_cookies(response, response.request)
            URL = (
                'http://www.gretai.org.tw/web/stock/aftertrading/' +
                'broker_trading/download_ALLCSV.php?' +
                'curstk=%(stock)s&stk_date=%(date)s') % {
                'stock': item['stockid'],
                'date': date
            }

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

#    def parse_after_csv_find(self):
