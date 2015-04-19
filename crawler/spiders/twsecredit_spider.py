# -*- coding: utf-8 -*-

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log


#__all__ = ['TwseCreditSpider']
##
## 融券/融券 { 前日餘額, 賣出, 買進, 現券, 今日餘額, 限額 }
#
## 融資: http://www.twse.com.tw/ch/trading/exchange/TWTA1U/TWTA1U.php
## 融券: http://www.twse.com.tw/ch/trading/exchange/TWT93U/TWT93U.php
#class TwseCreditSpider(CrawlSpider):
#    name = 'twsecredit'
#    allowed_domains = ['http://twse.com.tw']
#    _headers = [
#        [()]
#        [
#    @classmethod
#    def from_crawler(cls, crawler):
#        return cls(crawler)
#
