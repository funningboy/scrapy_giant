# -*- coding: utf-8 -*-

from crawler.pipelines.twsehisfuture_pipeline import TwseHisFuturePipeline
from handler.hisdb_handler import *

__all__ = ['OtcHisFuturePipeline']

class OtcHisFuturePipeline(TwseHisFuturePipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcHisFuturePipeline, self).__init__(crawler)
        self._name = 'otchisfuture'
        kwargs = {
            'debug': crawler.settings.getbool('GIANT_DEBUG'),
            'opt': 'otc'
        }
        self._db = OtcHisDBHandler(**kwargs)
