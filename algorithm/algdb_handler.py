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

__all__ [
    'TwseDualemaAlg',
    'OtcDualemaAlg',
#    'TwseBestTraderAlg',
#    'OtcBestTraderAlg',
#    'TwseBBandsAlg',
#    'OtcBBandsAlg'

    ]

class TwseAlgDBHandler(object):

    def __init__(self, *args, **kwargs):
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('twsealgdb', host=host, port=port, alias='twsealgdb')
        self._coll = switch(TwseAlgColl, 'twsealgdb')
        self._alg = None
        self._dbhandler = hisdb_tasks['twse']()
        self._idhandler = iddb_tasks['twse']()
        self._report = Report(
            sort=[('buy_count', False), ('sell_count', False), ('volume', False)], limit=20)

    def run(self):
        pass

    def insert(self, item):
        for it in item:
        cursor = self._coll.objects(Q(date=))
        cursor = list(cursor)
        coll = self._coll.save() else cursor[0]
        coll.date =
        coll.algnm = self._alg.__class__.__name__
        data = {
            portfolio_value:
            ending_value:
            ending_cash:
            buy_count:
            sell_count:
        }
        coll.datalist =

    def delete(self):
        pass

    def query(self, time=datetime.utcnow(), stockids=[], traderids=[], portfolio=0):
        coll = self._coll
            coll = coll.objects(Q(date=time))
        coll.objects(Q(__))
        return


class TwseDualemaAlg(TwseAlgDBHandler):

    def __init__(self, *args, **kwargs):
        self._maxlen = kwargs.pop('maxlen', 30)
        super(TwseDualemaAlg, self).__init__(args, kwargs)
        self._alg = DualEMAAlgorithm

    def run(self, starttime, endtime, stockids=[], traderids=[], order='totalvolume', limit=10):
        args = (starttime, endtime, stockids, traderids, order, limit)
        for stockid in stockids:
            self._dbhandler.stock.drop()
            self._dbhandler.trader.drop()
            self._dbhandler.stcok.ids = [stockid]
            self._dbhandler.trader.ids = [traderid]
            data = dbhandler.transform_all_data(*args)
            if len(data[stockid].index) < self._maxlen:
                continue
            alg = self._alg(self._dbhandler)
            results = alg.run(data).fillna(0)
            self._report.collect("%s" %(stockid), results)
        return self._report.summary(dtype='dict')


class TwseBestTraderAlg(TwseAlgHandler):

    def __init__(self, *args, **kwargs):
        self._maxlen = kwargs.pop('maxlen', 10)
        super(TwseBestTraderAlg, self).__init__(args, kwargs)

    def run(self, starttime, endtime, stockids=[], traderids=[], order='totalvolume', limit=10):
        args = (starttime, endtime, stockids, traderids, order, limit)
        for traderid in traderids:
            for stockid in stockids:
                self._dbhandler.stock.drop()
                self._dbhandler.trader.drop()
                self._dbhandler.stcok.ids = [stockid]
                self._dbhandler.trader.ids = [traderid]
                data = dbhandler.transform_all_data(*args)
                if len(data[stockid].index) < self._maxlen:
                    continue
                alg = self._alg(self._dbhandler)
                results = alg.run(data).fillna(0)
                self._report.collect("%s-%s" %(traderid, stockid), results)
        return self._report.summary(dtype='dict')
