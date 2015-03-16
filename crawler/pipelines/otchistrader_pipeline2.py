# -*- coding: utf-8 -*-

from crawler.pipelines.otchistrader_pipeline import OtcHisTraderPipeline

__all__ = ['OtcHisTraderPipeline2']

class OtcHisTraderPipeline2(OtcHisTraderPipeline):

    def __init__(self, crawler):
        super(OtcHisTraderPipeline2, self).__init__(crawler)
        self._name = 'otchistrader2'
