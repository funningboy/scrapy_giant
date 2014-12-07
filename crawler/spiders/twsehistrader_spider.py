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

    def run_pytesser_perdition(url):
        response = urllib2.open(url)
        arr = np.asarray(bytearray(response.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1) # 'load it as it is'
        # gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # smooth noise
        blur = cv2.GaussianBlur(gray,(5,5),0)
        # threshold filter
        ret,th1 = cv2.threshold(blur,223,255,cv2.THRESH_BINARY)
        return pytesser.iplimage_to_string(cv.fromarray(th1))

    def try_predict_captcha(self, url, loop=5):
        record = []
        for i in xrange(loop):
            try:
                text = run_pytesser_perdition(url).strip()
                if len(text) == 5:
                    record.append(text)
                time.sleep(0.5)
            except Exception:
                time.sleep(2)
                pass
        return Counter(record).most_common(1)[0][0] if record else ''

    def parse(self, response):
        """ override level 0 """
        item = response.meta['item']
        sel = Selector(response)
        # get asp cookie contents for sumbit form
        url = sel.xpath('.//td/div/div/img/@src').extract()[0]
        contents = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': sel.xpath('.//input[@id="__VIEWSTATE"]/@value').extract()[0],
            '__EVENTVALIDATION': sel.xpath('.//input[@id="__EVENTVALIDATION"]/@value').extract()[0],
            'RadioButton_Normal': 'RadioButton_Normal',
            'TextBox_Stkno': item['stockid'],
            'CaptchaControl1': self.try_predict_captcha(url),
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
            # register next response handler after csv was found
            find = self.xpath('.//a[@id="HyperLink_DownloadCSV"]/@href')
            request = Request(
                URL,
                callback=self.parse_after_csv_find,
                dont_filter=True)
            request.meta['item'] = item
            yield request
        except:
            if
                request = Request(
                    URL,
                    callback=self.parser
                    dont_filter=True)
            else:
                log.msg("fetch %s fail" % (item['stockid']), log.INFO)
            return

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
        yield item
