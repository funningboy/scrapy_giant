# -*- coding: utf-8 -*-


#from scrapy.selector import Selector
#from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy import Request, FormRequest
#from scrapy import log
#from crawler.items import TwseHisFutureItem
#
#from handler.iddb_handler import TwseIdDBHandler
#
#__all__ = ['TwseHisFutureSpider']
#
#class TwseHisFutureSpider(CrawlSpider):
#    name = 'twsehisfuture'
#
#
#    @classmethod
#    def from_crawler(cls, crawler):
#        return cls(crawler)
#
#    def __init__(self, crawler):
#        super(TwseHisStockSpider, self).__init__()
#        kwargs = {
#            'debug': crawler.settings.getbool('GIANT_DEBUG'),
#            'limit': crawler.settings.getint('GIANT_LIMIT'),
#            'opt': 'twse'
#        }
#        self._id = TwseIdDBHandler(**kwargs)
#
#    def start_requests(self):
#        pass
