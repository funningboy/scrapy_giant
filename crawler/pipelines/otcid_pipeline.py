# -*- coding: utf-8 -*-

from crawler.pipelines.twseid_pipeline import TwseIdPipeline
from query.iddb_query import *

__all__ = ['OtcIdPipeline']

class OtcIdPipeline(TwseIdPipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(OtcIdPipeline, self).__init__(crawler)
        self._name = 'otcid'
        self._db = OtcIdDBQuery()
