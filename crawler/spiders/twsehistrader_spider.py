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
import urllib2

from handler.iddb_handler import TwseIdDBHandler
from crawler.spiders.twsehistrader_captcha import TwseHisTraderCaptcha0

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

    def predict_captcha(self, url, loop=3):
        record = []
        #try:
        for i in xrange(loop):
            response = urllib2.open(url)
            arr = np.asarray(bytearray(response.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1)
            print img
            text = TwseHisTraderCaptcha0().run(img)
            if len(text) == 5:
                record.append(text)
            print text
        #except Exception:
        #    pass
        return Counter(record).most_common(1)[0][0] if record else ''

    def parse(self, response):
        """ override level 0 """
        item = response.meta['item']
        sel = Selector(response)
        # get asp cookie contents for sumbit form
        url = sel.xpath('.//td/div/div/img/@src').extract()[0]
        print url
        contents = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': sel.xpath('.//input[@id="__VIEWSTATE"]/@value').extract()[0],
            '__EVENTVALIDATION': sel.xpath('.//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
            'RadioButton_Normal': 'RadioButton_Normal',
            'TextBox_Stkno': item['stockid'],
            'CaptchaControl1': self.predict_captcha(url),
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
            URL = self._domain + '/bshtm/bsContent.aspx'
            # register next response handler after csv was found
            find = self.xpath('.//a[@id="HyperLink_DownloadCSV"]/@href')
            request = Request(
                URL,
                callback=self.parse_after_csv_find,
                dont_filter=True)
            request.meta['item'] = item
            yield request
        except:
            URL = 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx'
            request = Request(
                URL,
                callback=self.parse,
                dont_filter=True)
            request.meta['item'] = item
            yield request

    def parse_after_csv_find(self, response):
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
        yield item
