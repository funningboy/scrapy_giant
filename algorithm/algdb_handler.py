# -*- coding: utf-8 -*-

import pandas as pd
import pytz
from collections import OrderedDict
from bson import json_util

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.tasks import hisdb_tasks, iddb_tasks
from algorithm.models import *
from algorithm.report import Report
from algorithm.dualema import DualEMAAlgorithm
from algorithm.besttrader import BestTraderAlgorithm
from algorithm.bbands import BBandsAlgorithm
from algorithm.randforest import RandForestAlgorithm
#from algorithm.kdtree import KdtKnnAlgorithm
#from algorithm.kmeans import

# register all alg to algdb_handler via decorator
__all__ = [
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
    DualEMAAlgorithm: 'dualemadb',
    BestTraderAlgorithm: 'btraderdb',
    BBandsAlgorithm: 'bbandsdb',
    RandForestAlgorithm: 'rforestdb',
}

class TwseAlgDBHandler(object):

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        db = "twse%s" %(algdbmap[self._alg])
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumy_coll = switch(TwseAlgSummaryColl, db)
        self._detl_coll = switch(TwseAlgDetailColl, db)
        self._dbhandler = hisdb_tasks['twse']()
        self._idhandler = iddb_tasks['twse']()
        self._report = Report(
            sort=[('buy_count', False), ('sell_count', False), ('portfolio_value', False)], limit=20)

    @property
    def dbhandler(self):
        return self._dbhandler

    @property
    def idhandler(self):
        return self._idhandler

    def run(self):
        pass

    def delete(self):
        pass

    def drop_detail(self):
        self._detl_coll.drop_collection()

    def drop_summary(self):
        self._sumy_coll.drop_collection()

    def to_summary(self, df):
        keys = [k for k,v in AlgSummaryColl._fields.iteritems()]
        for ix, cols in df.iterrows():
            stockid = ix
            cursor = self._sumy_coll.objects(Q(end_time=cols['end_time']) & Q(stockid=stockid))
            cursor = list(cursor)
            coll = self._sumy_coll() if len(cursor)==0 else cursor[0]
            coll.start_time = cols['start_time']
            coll.end_time = cols['end_time']
            coll.stockid = stockid
            coll.portfolio_value = cols['portfolio_value']
            coll.ending_value = cols['ending_value']
            coll.ending_cash = cols['ending_cash']
            coll.capital_used = cols['capital_used']
            coll.buy_count = cols['buy_count']
            coll.sell_count = cols['sell_count']
            coll.save()

    def to_detail(self, df):
        self.drop_detail()
        for ix, cols in df.iterrows():
            coll = self._detl_coll()
            coll.time = ix
            coll.open = cols['open']
            coll.high = cols['high']
            coll.low = cols['low']
            coll.close = cols['close']
            coll.volume = cols['volume']
            coll.portfolio_value = cols['portfolio_value']
            coll.ending_value = cols['ending_value']
            coll.ending_cash = cols['ending_cash']
            coll.capital_used = cols['capital_used']
            coll.buy = cols['buy']
            coll.sell = cols['sell']
            coll.save()

    def query_summary(self, time=None, stockids=[], traderids=[], **kwargs):
        keys = [k for k,v in AlgSummaryColl._fields.iteritems()]
        cursor = self._sumy_coll.objects.all()
        if time:
            cursor = cursor(Q(end_time=time))
        if stockids:
            cursor = cursor(Q(stockid__in=stockids))
        if traderids:
            cursor = cursor(Q(traderid__in=traderids))
        for k in keys:
            v = kwargs.pop(k, None)
            if v:
                c = {"%s__gt" %(k): v}
                # __lt
                cursor = cursor(Q(**c))
        return list(cursor)


    def query_detail(self):
        cursor = self._detl_coll.objects.all()
        return list(cursor)


class OtcAlgDBHandler(TwseAlgDBHandler):

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        db = "otc%s" %(algdbmap[self._alg])
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumy_coll = switch(OtcAlgSummaryColl, db)
        self._detl_coll = switch(OtcAlgDetailColl, db)
        self._dbhandler = hisdb_tasks['otc']()
        self._idhandler = iddb_tasks['otc']()
        self._report = Report(
            sort=[('buy_count', False), ('sell_count', False), ('portfolio_value', False)], limit=20)


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
            self._dbhandler.stock.ids = [stockid]
            data = self._dbhandler.transform_all_data(*args)
            alg = self._alg(dbhandler=self._dbhandler)
            results = alg.run(data).fillna(0)
            self._report.collect("%s" %(stockid), results)
        if callback == self.to_summary:
            return callback(self._report.summary())
        elif callback == self.to_detail:
            return callback(self._report.iter_report(stockid))
        else:
            return self._report.summary()


class OtcDualemaAlg(OtcAlgDBHandler):

    def __init__(self, *args, **kwargs):
        self._alg = DualEMAAlgorithm
        super(OtcDualemaAlg, self).__init__(args, kwargs)


class TwseBestTraderAlg(TwseAlgDBHandler):

    def __init__(self, *args, **kwargs):
        self._alg = BestTraderAlgorithm
        super(TwseBestTraderAlg, self).__init__(args, kwargs)

    def run(self, starttime, endtime, stockids=[], traderids=[],
            order='totalvolume', limit=10, callback=None):
        args = (starttime, endtime, stockids, traderids, order, limit)
        if callback == self.to_detail:
            assert(len(traderids)==1)
        for traderid in traderids:
            for stockid in stockids:
                self._dbhandler.stock.drop()
                self._dbhandler.trader.drop()
                self._dbhandler.stock.ids = [stockid]
                self._dbhandler.trader.ids = [traderid]
                data = self._dbhandler.transform_all_data(*args)
                alg = self._alg(dbhandler=self._dbhandler)
                results = alg.run(data).fillna(0)
                self._report.collect("%s-%s" %(traderid, stockid), results)
        if callback == self.to_summary:
            return callback(self._report.summary())
        elif callback == self.to_detail:
            return callback(self._report.iter_report("%s-%s" %(traderid, stockid)))
        else:
            return self._report.summary()


class OtcBestTraderAlg(OtcAlgDBHandler):

    def __init__(self, *args, **kwargs):
        self._alg = BestTraderAlgorithm
        super(OtcBestTraderAlg, self).__init__(args, kwargs)


class TwseBBandsAlg(TwseDualemaAlg):

    def __init__(self, *args, **kwargs):
        self._alg = BBandsAlgorithm
        super(TwseBBandsAlg, self).__init__(args, kwargs)


class OtcBBandsAlg(OtcDualemaAlg):

    def __init__(self, *args, **kwargs):
        self._alg = BBandsAlgorithm
        super(OtcBBandsAlg, self).__init__(args, kwargs)


class TwseRandForestAlg(TwseDualemaAlg):

    def __init__(self, *args, **kwargs):
        self._alg = RandForestAlgorithm
        super(TwseRandForestAlg, self).__init__(args, kwargs)


class OtcRandForestAlg(OtcDualemaAlg):

    def __init__(self, *args, **kwargs):
        self._alg = RandForestAlgorithm
        super(OtcRandForestAlg, self).__init__(args, kwargs)
