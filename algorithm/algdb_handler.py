# -*- coding: utf-8 -*-

import pandas as pd
import pytz
from collections import OrderedDict
from datetime import datetime, timedelta

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.tasks import *
from algorithm.models import *
from algorithm.report import Report
from algorithm.dualema import DualEMAAlgorithm
from algorithm.besttrader import BestTraderAlgorithm
from algorithm.bbands import BBandsAlgorithm
#from algorithm.randforest import RandForestAlgorithm
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
#    'TwseRandForestAlg',
#    'OtcRandForestAlg'
    ]

# alg db map
algdbmap = {
    DualEMAAlgorithm: 'dualemadb',
    BestTraderAlgorithm: 'btraderdb',
    BBandsAlgorithm: 'bbandsdb',
#    RandForestAlgorithm: 'rforestdb',
}

class TwseAlgDBHandler(object):
    """
    """
    def __init__(self, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._cfg = kwargs.pop('cfg', {'debug': self._debug, 'buf_win': 30})
        db = "twse%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._report = Report(sort=[('buy_count', False), ('sell_count', False), ('portfolio_value', False)], limit=100)
        self._collect = default_hiscollect(**kwargs)

    def run(self):
        pass

    def delete_summary(self, item):
        pass

    @property
    def sumycoll(self):
        return self._sumycoll

    def to_summary(self, df):
        keys = [k for k,v in AlgSummaryColl._fields.iteritems()]
        for ix, cols in df.iterrows():
            stockid = ix
            cursor = self._sumycoll.objects(Q(end_time=cols['end_time']) & Q(stockid=stockid))
            coll = self._sumycoll() if len(cursor) == 0 else cursor[0]
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
        retval = []
        for ix, cols in df.iterrows():
            coll = {
                'time': ix,
                'open': cols['open'],
                'high': cols['high'],
                'low': cols['low'],
                'close': cols['close'],
                'volume': cols['volume'],
                'portfolio_value': cols['portfolio_value'],
                'ending_value': cols['ending_value'],
                'ending_cash': cols['ending_cash'],
                'capital_used': cols['capital_used'],
                'buy': cols['buy'],
                'sell': cols['sell']
            }
            retval.append(coll)
        return retval

    def query_summary(self, time=None, stockids=[], traderids=[], **kwargs):
        keys = [k for k,v in AlgSummaryColl._fields.iteritems()]
        cursor = self._sumycoll.objects.all()
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
        pass


class TwseDualemaAlg(TwseAlgDBHandler):
    """
    >>>
    >>> alg = TwseDualemaAlg(debug=True)
    >>> item = alg.run(starttime, endtime, ['2317'], alg.to_detail)
    >>> print item
    """

    def __init__(self, **kwargs):
        self._alg = DualEMAAlgorithm
        super(TwseDualemaAlg, self).__init__(**kwargs)

    def run(self, starttime, endtime, stockids=[], callback=None):
        for stockid in stockids:
            self._collect['frame']['hisstock'].update({
                'starttime': starttime,
                'endtime': endtime,
                'stockids': [stockid],
            })
            data, db = collect_hisframe(**self._collect)
            if not data.empty and db:
                if len(data[stockid].index) < self._cfg['buf_win']:
                    continue
                alg = self._alg(dbhandler=db, **self._cfg)
                results = alg.run(data).fillna(0)
                self._report.collect("%s" %(stockid), results)

        if callback == self.to_summary:
            return callback(self._report.summary())
        if callback == self.to_detail:
            return callback(self._report.iter_report(stockid))
        return self._report.summary()


class TwseBestTraderAlg(TwseAlgDBHandler):
    """
    # find trader
    >>> starttime = datetime.utcnow() - timedelta(days=10)
    >>> endtime = datetime.utcnow()
    >>> kwargs = {'debug': True, 'opt': otc}
    >>> dbhandler = TwseHisDBHandler(**kwargs)
    >>> args = (starttime, endtime, ['2317'], [], 'stock', ['-totalvolume'], 10)
    >>> dbhandler.trader.query_raw(*args)
    >>> tops = list(dbhandler.trader.get_alias(['2317'], 'trader', ["top%d" %i for i in range(10)]))
    >>> print "%s" %(tops)
    # run alg
    >>> alg = TwseBestTraderAlg(debug=True)
    >>> item = alg.run(starttime, endtime, ['2317'], tops, alg.to_detail)
    >>> print item
    """

    def __init__(self, **kwargs):
        self._alg = BestTraderAlgorithm
        super(TwseBestTraderAlg, self).__init__(**kwargs)

    def run(self, starttime, endtime, stockids=[], traderids=[], callback=None):
        for stockid in stockids:
            for traderid in traderids:
                self._collect['frame']['histrader'].updte({
                    'starttime': starttime,
                    'endtime': endtime,
                    'stockids': [stockid],
                    'traderids': [traderid]
                })
                data, db = collect_hisframe(**self._collect)
                if not data.empty or db:
                    if len(data[stockid].index) < self._cfg['buf_win']:
                        continue
                    alg = self._alg(dbhandler=db, **self._cfg)
                    results = alg.run(data).fillna(0)
                    self._report.collect("%s-%s" %(traderid, stockid), results)

        if callback == self.to_summary:
            return callback(self._report.summary())
        if callback == self.to_detail:
            return callback(self._report.iter_report("%s-%s" %(traderid, stockid)))
        return self._report.summary()


class TwseBBandsAlg(TwseAlgDBHandler):
    """
    """

    def __init__(self, **kwargs):
        self._alg = BBandsAlgorithm
        super(TwseBBandsAlg, self).__init__(**kwargs)

    def run(self, starttime, endtime, stockids=[], callback=None):
        for stockid in stockids:
            self._collect['frame']['hisstock'].update({
                'starttime': starttime,
                'endtime': endtime,
                'stockids': [stockid],
            })
            data, db = collect_hisframe(**self._collect)
            if not data.empty and db:
                if len(data[stockid].index) < self._cfg['buf_win']:
                    continue
                alg = self._alg(dbhandler=db, **self._cfg)
                results = alg.run(data).fillna(0)
                self._report.collect("%s" %(stockid), results)

        if callback == self.to_summary:
            return callback(self._report.summary())
        if callback == self.to_detail:
            return callback(self._report.iter_report(stockid))
        return self._report.summary()


class OtcDualemaAlg(TwseDualemaAlg):

    def __init__(self, **kwargs):
        super(OtcDualemaAlg, self).__init__(**kwargs)
        db = "otc%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)


class OtcBestTraderAlg(TwseBestTraderAlg):

    def __init__(self, **kwargs):
        super(OtcBestTraderAlg, self).__init__(**kwargs)
        db = "otc%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)

class OtcBBandsAlg(TwseBBandsAlg):

    def __init__(self, **kwargs):
        super(OtcBBandsAlg, self).__init__(**kwargs)
        db = "otc%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)

