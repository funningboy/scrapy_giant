
# -*- coding: utf-8 -*-

from crawler.pipelines.twsehistrader_pipeline import TwseHisTraderPipeline
from query.hisdb_query import *
from query.iddb_query import *

__all__ = ['OtcHisTraderPipeline']

class OtcHisTraderPipeline(TwseHisTraderPipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcHisTraderPipeline, self).__init__(crawler)
        self._name = 'otchistrader'
        self._db = OtcHisDBQuery()
        self._tr = TraderIdDBQuery()
