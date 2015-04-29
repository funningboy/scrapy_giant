# -*- coding: utf-8 -*-

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from crawler.items import OtcHisCreditItem

__all__ = ['OtcHisCreditSpider']

# http://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal.php?l=zh-tw
# 融資 融券

#class OtcHisCreditSpider(CrawlSpider):
#    name = 'otc
#    allowed_domains = ['
#    download_delay = 2
#    _headers = [
#    ]
#
