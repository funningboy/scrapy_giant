# -*- coding: utf-8 -*-

from crawler.pipelines.twsehiscredit_pipeline import TwseHisCreditPipeline
from handler.hisdb_handler import *

__all__ = ['OtcHisCreditPipeline']

class OtcHisCreditPipeline(TwseHisCreditPipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcHisCreditPipeline, self).__init__(crawler)
        self._name = 'otchiscredit'
        kwargs = {
            'debug': crawler.settings.getbool('GIANT_DEBUG'),
            'opt': 'otc'
        }
        self._db = OtcHisDBHandler(**kwargs)
