# -*- coding: utf-8 -*-
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
from crawler.items import OtcHisTraderItem
from crawler.spiders.otchistrader_captcha import OtcHisTraderCaptcha1

from handler.iddb_handler import OtcIdDBHandler

__all__ = ['OtcHisTraderSpider']

class OtcHisTraderSpider(CrawlSpider):
    name = 'otchistrader'
    allowed_domains = ['http://www.gretai.org.tw']
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
        super(OtcHisTraderSpider, self).__init__()
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
            URL = 'http://www.gretai.org.tw/web/stock/aftertrading/broker_trading/brokerBS.php?l=zh-tw'
            item = OtcHisTraderItem()
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
        URL = 'http://www.gretai.org.tw/web/inc/authnum.php'
        request = Request(
           URL,
            meta={
                'item': item,
                'cookiejar': response.meta['cookiejar']
            },
            callback=self.parse_after_captcha_find,
            dont_filter=True)
        yield request

    def parse_after_captcha_find(self, response):
        item = response.meta['item']
        # use captcha alg as text decode
        arr = np.asarray(bytearray(response.body), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        text = OtcHisTraderCaptcha1(False).run(img)
        #text = raw_input('test:')
        #print text
        content = {
            'auth_num': text,
            'stk_code': item['stockid']
        }
        URL = 'http://www.gretai.org.tw/web/stock/aftertrading/broker_trading/brokerBS.php?l=zh-tw'
        request = FormRequest(
            URL,
            meta={
                'item': item,
                'cookiejar': response.meta['cookiejar'],
                'content': content
            },
            formdata=content,
            callback=self.parse_after_form_submit,
            dont_filter=True)
        yield request

    def parse_after_form_submit(self, response):
        item, content = response.meta['item'], response.meta['content']
        sel = Selector(response)
        err = sel.xpath('/html/body/center/div[3]/div[2]/div[4]/div/p/text()').extract()
        if err:
            if re.match(ur'.*驗證碼錯誤.*', err[0], re.UNICODE):
                URL = 'http://www.gretai.org.tw/web/stock/aftertrading/broker_trading/brokerBS.php?l=zh-tw'
                item['count'] += 1
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
                log.msg("fetch %s null" % (item['stockid']), level=log.INFO)
                return
        else:
            date = sel.xpath('.//tr[1]/td[2]/text()').extract()[0]
            stk_date = re.findall(r'\d+', date)
            URL = (
                'http://www.gretai.org.tw/web/stock/aftertrading/' +
                'broker_trading/download_ALLCSV.php?' +
                'curstk=%(stock)s&stk_date=%(date)s&auth=%(auth)s') % {
                'stock': item['stockid'],
                'date': ''.join(stk_date),
                'auth': content['auth_num']
            }
            yy, mm, dd = map(int, stk_date)
            item['date'] = "%s-%s-%s" % (1911+yy, mm, dd)
            request = Request(
                URL,
                meta = {
                    'item': item,
                    'cookiejar': response.meta['cookiejar']
                },
                callback=self.parse_after_page_find,
                dont_filter=True)
            yield request

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
