# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy import log
from crawler.items import TraderIdItem

__all__ = ['TraderIdSpider']

class TraderIdSpider(CrawlSpider):
    name = 'traderid'
    allowed_domains = ['http://www.twse.com.tw']
    download_delay = 2

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TraderIdSpider, self).__init__()

    def start_requests(self):
        URLS = [
            'http://www.twse.com.tw/ch/products/broker_service/broker_list.php',
            'http://www.twse.com.tw/ch/products/broker_service/broker2_list.php'
        ]
        for i, URL in enumerate(URLS):
            item = TraderIdItem()
            item['data'] = []
            request = Request(
                URL,
                meta={
                    'item': item
                },
                callback=self.parse0 if i == 0 else self.parse1,
                dont_filter=True)
            yield request

    def parse0(self, response):
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        sel = Selector(response)
        item = response.meta['item']
        elems = sel.xpath('.//*[@id="main-content"]//tr')
        for elem in elems[1:]:
            traderid = elem.xpath('.//td[1]/text()').extract()[0]
            tradernm = elem.xpath('.//td[2]/a/text()').extract()[0]
            sub = {
                'traderid': traderid,
                'tradernm': tradernm.replace(' ','').replace('-','')
            }
            item['data'].append(sub)
        log.msg("item[0] %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item

    def parse1(self, response):
        log.msg("URL: %s" % (response.url), level=log.DEBUG)
        sel = Selector(response)
        item = response.meta['item']
        elems = sel.xpath('.//table[@class="board_prod"]//tr')
        for elem in elems[1:]:
            traderid = elem.xpath('.//td[1]/text()').extract()[0]
            tradernm = elem.xpath('.//td[2]/a/text()').extract()[0]
            sub = {
                'traderid': traderid,
                'tradernm': tradernm.replace(' ','').replace('-','')
            }
            item['data'].append(sub)
        log.msg("item[0] %s ..." % (item['data'][0]), level=log.DEBUG)
        yield item
