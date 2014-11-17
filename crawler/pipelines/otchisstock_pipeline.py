# -*- coding: utf-8 -*-

from crawler.pipelines.twsehisstock_pipeline import TwseHisStockPipeline
from handler.hisdb_handler import *

__all__ = ['OtcHisStockPipeline']

class OtcHisStockPipeline(TwseHisStockPipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcHisStockPipeline, self).__init__(crawler)
        self._name = 'otchisstock'
        self._settings = crawler.settings
        self._db = OtcHisDBHandler()
