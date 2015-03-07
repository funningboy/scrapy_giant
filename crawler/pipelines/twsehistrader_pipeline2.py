# -*- coding: utf-8 -*-

from crawler.pipelines.twsehistrader_pipeline import TwseHisTraderPipeline

__all__ = ['TwseHisTraderPipeline2']

class TwseHisTraderPipeline2(TwseHisTraderPipeline):

    def __init__(self, crawler):
        super(TwseHisTraderPipeline2, self).__init__(crawler)
        self._name = 'twsehistrader2'
