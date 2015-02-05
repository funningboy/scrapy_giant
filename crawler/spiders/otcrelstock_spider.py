# -*- coding: utf-8 -*-
#
import re
import pandas as pd

from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request, FormRequest
from scrapy.http.cookies import CookieJar
from scrapy import log
from crawler.items import OtcRelStockItem

from handler.iddb_handler import OtcIdDBHandler

__all__ = ['OtcRelStockSpider']

class OtcRelStockSpider(CrawlSpider):
    pass

