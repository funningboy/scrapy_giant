# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

from scrapy import log
from crawler.pipelines.base_pipeline import BasePipeline
from handler.iddb_handler import *

__all__ = ['TraderIdPipeline']

class TraderIdPipeline(BasePipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TraderIdPipeline, self).__init__()
        self._name = 'traderid'
        self._settings = crawler.settings
        self._id = TwseIdDBHandler()

    def process_item(self, item, spider):
        if spider.name not in [self._name]:
            return item
        item = self._clear_item(item)
        item = self._update_item(item)
        self._write_item(item)

    def _clear_item(self, item):
        jstream = self._encode_item(item)
        return self._decode_item(jstream)

    def _update_item(self, item):
        item = item['data']
        log.msg("item: %s" % (item), level=log.DEBUG)
        return item

    def _write_item(self, item):
        self._id.trader.insert(item)
