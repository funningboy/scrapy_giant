# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pytz
from datetime import datetime

from scrapy import log
from crawler.pipelines.base_pipeline import BasePipeline
from handler.hisdb_handler import *

__all__ = ['TwseHisCreditPipeline']

class TwseHisFuturePipeline(BasePipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TwseHisFuturePipeline, self).__init__()
        self._name = 'twsehisfuture'
        kwargs = {
            'debug': crawler.settings.getbool('GIANT_DEBUG'),
            'opt': 'twse'
        }
        self._db = TwseHisDBHandler(**kwargs)

    def process_item(self, item, spider):
        if spider.name not in [self._name]:
            return item
        item = self._clear_item(item)
        item = self._update_item(item)
        self._write_item(item)

    def _clear_item(self, item):
        jstream = self._encode_item(item)
        return self._decode_item(jstream)
