# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pytz
from datetime import datetime

from scrapy import log
from crawler.pipelines.base_pipeline import BasePipeline
from query.hisdb_query import *

__all__ = ['TwseHisTraderPipeline']

class TwseHisTraderPipeline(BasePipeline):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        super(TwseHisTraderPipeline, self).__init__()
        self._settings = crawler.settings
        self._name = 'twsehistrader'
        self._db = TwseHisDBQuery()

    def process_item(self, item, spider):
        if spider.name not in [self._name]:
            return item
        item = self._clear_item(item)
        item = self._update_item(item, 30 if not self._settings.getbool('GIANT_DEBUG') else 1)
        self._write_item(item)

    def _clear_item(self, item):
        jstream = self._encode_item(item)
        return self._decode_item(jstream)

    def _update_item(self, item, top=30):
        # create raw pdframe
        frame = pd.DataFrame.from_dict(item['traderlist']).dropna()
        # sort and divided pdframe
        stream = []
        grouped = frame.groupby('traderid', sort=False)
        for trdid, group in grouped:
            trdid = group['traderid'].iloc[0]
            trdnm = group['tradernm'].iloc[0]
            buyvolume = group['buyvolume'].astype(int).sum() // 1000
            sellvolume = group['sellvolume'].astype(int).sum() // 1000
            avgbuyprice = sum([it[0] * it[1] for it in zip(group['price'].astype(float), group['buyvolume'].astype(int) // 1000)]) // buyvolume
            avgsellprice = sum([it[0] * it[1] for it in zip(group['price'].astype(float), group['sellvolume'].astype(int) // 1000)]) // sellvolume
            trdser = pd.Series([
                trdid,
                trdnm,
                avgbuyprice,
                buyvolume,
                avgsellprice,
                sellvolume],
                index=[
                    'traderid',
                    'tradernm',
                    'avgbuyprice',
                    'buyvolume',
                    'avgsellprice',
                    'sellvolume'])
            stream.append(trdser)
        frame = pd.DataFrame(stream).fillna(0)
        # divided frame to topbuy, topsell
        buyfm = frame.sort([
            'buyvolume',
            'avgbuyprice'], ascending=False)[0:top].fillna(0)
        sellfm = frame.sort([
            'sellvolume',
            'avgsellprice'], ascending=False)[0:top].fillna(0)
        # update item from frame
        buydct, selldct = buyfm.T.to_dict().values(), sellfm.T.to_dict().values()
        item['topbuylist'], item['topselllist'] = [], []
        for it in buydct:
            item['topbuylist'].append({
                'traderid': it['traderid'],
                'tradernm': it['tradernm'],
                'data': {
                    'avgbuyprice': it['avgbuyprice'],
                    'buyvolume': it['buyvolume'],
                    'avgsellprice': it['avgsellprice'],
                    'sellvolume': it['sellvolume']
                }
            })
        for it in selldct:
            item['topselllist'].append({
                'traderid': it['traderid'],
                'tradernm': it['tradernm'],
                'data': {
                    'avgbuyprice': it['avgbuyprice'],
                    'buyvolume': it['buyvolume'],
                    'avgsellprice': it['avgsellprice'],
                    'sellvolume': it['sellvolume']
                }
            })
        # update timestamp
        yy, mm, dd = item['date'].split('-')
        item['date'] = datetime(int(yy), int(mm), int(dd), 0, 0, 0, 0, pytz.utc)
        log.msg("item: %s" % (item), level=log.DEBUG)
        return item

    def _write_item(self, item):
        self._db.set_trader_data(item)
