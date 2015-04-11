# -*- coding: utf-8 -*-

import pandas as pd
import pytz
from collections import OrderedDict
from bson import json_util

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.tasks import *
from algorithm.models import *
from algorithm.dualema import DualEMAAlgorithm
from algorithm.besttrader import BestTraderAlgorithm
from algorithm.bbands import BBandsAlgorithm
from algorithm.randforest import RandForestAlgorithm

__all__ [
    'TwseDualemaAlg',
    'OtcDualemaAlg',
    'TwseBestTraderAlg',
    'OtcBestTraderAlg',
    'TwseBBandsAlg',
    'OtcBBandsAlg',
    'TwseRandForestAlg',
    'OtcRandForestAlg'
    ]

algdbmap = {
    DualEMAAlgorithm.__class__.__name__ : 'dualemadb',
    BestTraderAlgorithm.__class__.__name__: 'btraderdb',
    BBandsAlgorithm.__class__.__name__: 'bbandsdb',
    RandForestAlgorithm.__class__.__name__: 'rforestdb',
}

class TwseAlgDBHandler(object):

    def __init__(self, *args, **kwargs):
        assert(self._alg != None)
        db = "twse%s" %(algdbmap[self._alg.__class__.__name__])
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumy_coll = switch(TwseAlgSummaryColl, db)
        self._detl_coll = switch(TwseAlgDetailColl, db)
        self._dbhandler = hisdb_tasks['twse']()
        self._idhandler = iddb_tasks['twse']()
        self._report = Report(
            sort=[('buy_count', False), ('sell_count', False), ('portfolio_value', False)], limit=20)

    def run(self):
        pass

    def delete(self):
        pass

    def drop_detail()
        self._detl_coll.drop_collection()

    def drop_summary()
        self._sumy_coll.drop_collection()

    def to_summary(self, df):
        keys = [k for k,v in AlgSummaryColl._fields.iteritems()]
        for ix, cols in df.iterrows():
            cursor = self._sumy_coll.objects(Q(date=cols['end_time']) & (Q(stockid=cols['stockid']) | Q(traderid=cols['traderid'])))
            cursor = list(cursor)
            coll = self._sumy_coll.save() if len(cursor)==0 else cursor[0]
            dt = {k:cols[k] for k in df.columns if k in keys}
            dt.update({'stockid': ix})
            coll = AlgSummaryColl(**dt)
            coll.save()

    def to_detail(self, df):
        keys = []

    def query_summary(self, time=datetime.utcnow(), stockids=[], traderids=[], **kwargs):
        keys = [k for k,v in AlgSummaryColl._fields.iteritems()]
        cursor = self._sumy_coll.objects
        if time:
            cursor = cursor(Q(end_time==time))
        if stockids:
            cursor = cursor(Q(stockid__in=stockids))
        if traderids:
            cursor = cursor(Q(traderid__in=traderids))
        for k in keys:
            v = kwargs.pop(k, None)
            if v:
                c = {"%s__gt" %(k): v}
                cursor = cursor(Q(**c))
        return list(cursor)

    def query_detail():
        return .objects.all()

class TwseDualemaAlg(TwseAlgDBHandler):

    def __init__(self, *args, **kwargs):
        self._alg = DualEMAAlgorithm
        super(TwseDualemaAlg, self).__init__(args, kwargs)

    def run(self, starttime, endtime, stockids=[], traderids=[],
            order='totalvolume', limit=10, callback=None):
        args = (starttime, endtime, stockids, traderids, order, limit)
        if callback == self.to_detail:
            assert(len(stockids)==1)
        for stockid in stockids:
            self._dbhandler.stock.drop()
            self._dbhandler.trader.drop()
            self._dbhandler.stcok.ids = [stockid]
            self._dbhandler.trader.ids = [traderid]
            data = self._dbhandler.transform_all_data(*args)
            alg = self._alg(dbhandler=self._dbhandler, self._args, self._kwargs)
            results = alg.run(data).fillna(0)
            self._report.collect("%s" %(stockid), results)
        if callback == self.to_summary:
            return callback(self._report.summary())
        elif callback == self.to_detail:
            return callback(self._report.iter_report(stockid))
        else:
            return self._report.summary()

class TwseBestTraderAlg(TwseAlgHandler):

    def __init__(self, *args, **kwargs):
        self._alg = BestTraderAlgorithm
        super(TwseBestTraderAlg, self).__init__(args, kwargs)

    def run(self, starttime, endtime, stockids=[], traderids=[],
            order='totalvolume', limit=10, callback=self.insert_summary):
        args = (starttime, endtime, stockids, traderids, order, limit)
        if callback == self.insert_detail:
        for traderid in traderids:
            for stockid in stockids:
                self._dbhandler.stock.drop()
                self._dbhandler.trader.drop()
                self._dbhandler.stcok.ids = [stockid]
                self._dbhandler.trader.ids = [traderid]
                data = dbhandler.transform_all_data(*args)
                alg = self._alg(self._dbhandler)
                results = alg.run(data).fillna(0)
                self._report.collect("%s-%s" %(traderid, stockid), results)
        return self._report.summary(dtype='dict')
