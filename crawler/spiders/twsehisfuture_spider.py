# -*- coding: utf-8 -*-

# 期貨每日交易行情 http://59.120.135.101/chinese/3/3_1_1.asp
# 專有名詞 https://www.taifex.com.tw/chinese/9/9_2.asp
import re
import pandas as pd
import numpy as np
from StringIO import StringIO
from datetime import datetime, timedelta
import calendar

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import TwseHisFutureItem

from handler.iddb_handler import TwseIdDBHandler

__all__ = ['TwseHisFutureSpider']

class TwseHisFutureSpider(CrawlSpider):
    name = 'twsehisfuture'
    allowed_domains = ['www.taifex.com.tw']
    download_delay = 2
    _headers = [
        (u'交易日期', u'date'),
        (u'契約', u'contract'),
        (u'到期月份(週別)' u'contractmonth'),
        (u'開盤價', u'open'),
        (u'最高價', u'high'),
        (u'最低價', u'low'),
        (u'收盤價', u'close'),
        (u'成交量', u'volume'),
        (u'結算價', u'settlementprice'),
        (u'未沖銷契約數', u'untradecount'), 
        (u'最後最佳買價', u'bestbuy'),
        (u'最後最佳賣價', u'bestsell')
    ]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TwseHisFutureSpider, self).__init__()
        kwargs = {
            'debug': crawler.settings.getbool('GIANT_DEBUG'),
            'limit': crawler.settings.getint('GIANT_LIMIT'),
            'opt': 'twse'
        }
        self._id = TwseIdDBHandler(**kwargs)
        self._table = {}

    def start_requests(self):
        """ get contact """
        timestamp = datetime.utcnow()
        [fyear, syear] = [timestamp.year] * 2
        [fmon, smon] = [timestamp.month] * 2 
        [fdd, sdd] = [1, calendar.monthrange(timestamp.year, timestamp.month)[1]]
        URL = (
            'http://www.taifex.com.tw/chinese/3/3_1_1_getcontract.asp?' +
            'date1=%(fyear)d/%(fmon)02d/%(fdd)02d&' +
            'date2=%(syear)d/%(smon)02d/%(sdd)02d' ) % {
                'fyear': fyear, 
                'fmon': fmon,
                'fdd': fdd,
                'syear': syear,
                'smon': smon,
                'sdd': sdd
        }
        item = TwseHisFutureItem()
        request = Request(
            URL,
            meta={
                'item': item,
                'cookiejar': 0
            },
            callback=self.parse_contract_table,
            dont_filter=True)
        yield request

    def parse_contract_table(self, response):
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        sel = Selector(response)
        elems = sel.xpath('.//*[@id="commodity_id2t"]/option')
        # skip 請選擇, 全部
        for elem in elems[2:]:
            contract = elem.xpath('./text()').extract()[0].replace(u'\u3000', u'').replace(u' ', u'')
            identify = elem.xpath('./@value').extract()[0]
            m = re.search(r'([0-9a-zA-Z]{4,6})(\W+)\((\w+)\)', contract)
            if m:
                self._table.update({
                    m.group(1): identify
                })
        log.msg("table: %s" % str(self._table.items()[0]), level=log.INFO)
        
        # request after contract find
        URL = 'http://www.taifex.com.tw/chinese/3/3_1_2dl.asp'
        sdate = datetime.utcnow() - timedelta(days=3)
        edate = datetime.utcnow()
        datestart = "%d/%02d/%02d" %(sdate.year, sdate.month, sdate.day)
        dateend = "%d/%02d/%02d" %(edate.year, edate.month, edate.day)
        content = {
            'goday': '',
            'DATA_DATE': '',
            'DATA_DATE1': '',
            'DATA_DATE_Y': '',
            'DATA_DATE_M': '',
            'DATA_DATE_D': '',
            'DATA_DATE_Y1': '',
            'DATA_DATE_M1': '',
            'DATA_DATE_D1': '',
            'syear': '',
            'smonth': '',
            'sday': '',
            'syear1': '',
            'smonth1': '',
            'sday1': '',
            'datestart': datestart,
            'dateend': dateend,
            'COMMODITY_ID': 'specialid',
            'commodity_id2t': 'all',
            'his_year': "%d" %(edate.year)
        }
        request = FormRequest(
            URL,
            meta={
                'item': response.meta['item'],
                'content': content,
                'cookiejar': response.meta['cookiejar']
            },
            formdata=content,
            callback=self.parse_after_contract_find,
            dont_filter=True)
        yield request

    def parse_after_contract_find(self, response):
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        item = response.meta['item']
        item['url'] = response.url
        item['data'] = []
        try:
            frame = pd.read_csv(
                StringIO(response.body), delimiter=',',
                na_values=['--'], header=None, skiprows=[0], dtype=np.object).dropna()
            if frame.empty:
                log.msg("fetch %s empty" %('all'), log.INFO)
                return
        except:
            log.msg("fetch %s fail" %('all'), log.INFO)
            return
        for k, v in self._table.items():
            print frame[frame[1] == v].T.to_dict()



  
  
