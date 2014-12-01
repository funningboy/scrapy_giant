# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pytz
from datetime import datetime

from scrapy import log
from crawler.pipelines.base_pipeline import BasePipeline
from handler.hisdb_handler import *
from handler.iddb_handler import *

__all__ = ['TwseHisTraderPipeline']

class TwseHisTraderPipeline(BasePipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TwseHisTraderPipeline, self).__init__()
        self._settings = crawler.settings
        self._name = 'twsehistrader'
        self._db = TwseHisDBHandler()
        self._id = TwseIdDBHandler()

    def process_item(self, item, spider):
        if spider.name not in [self._name]:
            return item
        item = self._clear_item(item)
        item = self._update_item(item, 9999 if not self._settings.getbool('GIANT_DEBUG') else 3)
        self._write_item(item)

    def _clear_item(self, item):
        jstream = self._encode_item(item)
        return self._decode_item(jstream)

    def _update_item(self, item, top=100):
        # create raw pdframe
        frame = pd.DataFrame.from_dict(item['traderlist']).dropna()
        # sort and divided pdframe
        stream = []
        grouped = frame.groupby('traderid', sort=False)
        for trdid, group in grouped:
            trdid = group['traderid'].iloc[0]
#            trdnm = group['tradernm'].iloc[0]
            trdnm = filter(lambda x: x != '', group['tradernm'])[0]
            buyvolume = group['buyvolume'].astype(int).sum() // 1000
            sellvolume = group['sellvolume'].astype(int).sum() // 1000
            totalvolume = buyvolume + sellvolume
            avgbuyprice = sum([it[0] * it[1] for it in zip(group['price'].astype(float), group['buyvolume'].astype(int) // 1000)]) // buyvolume
            avgsellprice = sum([it[0] * it[1] for it in zip(group['price'].astype(float), group['sellvolume'].astype(int) // 1000)]) // sellvolume
            trdser = pd.Series([
                trdid,
                trdnm,
                avgbuyprice,
                buyvolume,
                avgsellprice,
                sellvolume,
                totalvolume],
                index=[
                    'traderid',
                    'tradernm',
                    'avgbuyprice',
                    'buyvolume',
                    'avgsellprice',
                    'sellvolume',
                    'totalvolume'])
            stream.append(trdser)
        frame = pd.DataFrame(stream).fillna(0)
        frame = frame.sort(['totalvolume'], ascending=False)[0:top]
        framedct = frame.T.to_dict().values()
        item['toplist'] = []
        for it in framedct:
            item['toplist'].append({
                'traderid': it['traderid'],
                'tradernm': it['tradernm'],
                'data': {
                    'avgbuyprice': it['avgbuyprice'],
                    'buyvolume': it['buyvolume'],
                    'avgsellprice': it['avgsellprice'],
                    'sellvolume': it['sellvolume'],
                    'totalvolume': it['totalvolume']
                }
            })
        yy, mm, dd = item['date'].split('-')
        item['date'] = datetime(int(yy), int(mm), int(dd), 0, 0, 0, 0, pytz.utc)
        log.msg("item: %s" % (item), level=log.DEBUG)
        return item

    def _write_item(self, item):
        self._db.trader.insert(item)
        self._id.trader.insert(item['toplist'])
