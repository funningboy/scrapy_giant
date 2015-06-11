# -*- coding: utf-8 -*-

import pandas as pd
import pytz
import copy
from collections import OrderedDict
from datetime import datetime, timedelta

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.table import default_hiscollect
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
        self._debug = kwargs.get('debug', False)
        assert(self._alg)
        self._cfg = {}
        db = "twse%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._collect = default_hiscollect(**kwargs)
        self._report = Report(sort=[('buys', False), ('sells', False), ('portfolio_value', False)], limit=100)

    @property
    def sumycoll(self):
        return self._sumycoll

    def iter_hisframe(self):
        for stockid in self._collect['stockids']:
            for k in ['hisstock', 'hiscredit', 'histrader']:
                self._collect['frame'][k].update({
                    'on': True,
                    'stockids': [stockid]
                    })
            data, handler = collect_hisframe(**copy.deepcopy(self._collect))
            yield stockid, data, handler

    def run(self, callback=None):            
        for stockid, data, dbhandler in self.iter_hisframe():
            if not data.empty and dbhandler:
                alg = self._alg(dbhandler, **self._cfg)
                results = alg.run(data).fillna(0)
                self._report.collect("%s" %(stockid), results)

        if callback == self.to_summary:
            return callback(self._report.summary())
        if callback == self.to_detail:
            return callback(self._report.iter_report(stockid))
        return self._report.summary()

    def delete_summary(self, item):
        pass

    def to_summary(self, df):
        keys = [k for k,v in AlgSummaryColl._fields.iteritems()]
        names = df.columns.values.tolist()
        for ix, cols in df.iterrows():
            stockid = ix
            cursor = self._sumycoll.objects(Q(endtime=cols['endtime']) & Q(stockid=stockid))
            coll = self._sumycoll() if len(cursor) == 0 else cursor[0]
            [setattr(coll, k, cols[k]) for k in names if k in keys]
            coll.stockid = stockid
            coll.save()

    def to_detail(self, df):
        retval = []
        keys = [k for k,v in AlgDetailColl._fields.iteritems()]
        names = df.columns.values.tolist()
        for ix, cols in df.iterrows():
            coll = {k:cols[k] for k in names if k in keys}
            retval.append(coll)
        return retval

    def query_summary(self, order=['-buys', 'sells', '-portfolio_value'], limit=10):
        """ return orm
        <algorithm>                               
        <endtime> |<bufwin> | <stockid> | <traderid> | buys | sells ...
        20140928  |  5      |  2330     |   null     | 100  | 100  
        20140929  | 10      |  2317     |  1440      | 99   | 99   
        """
        map_f = """
            function () {
                try {
                    var key =  { stockid : this.stockid };

                    };
                    emit(key, value);
                }
                catch(e){
                }
                finally{
                }
            }
        """
        reduce_f = """
        """
        finalize_f = """
        """
        #assert(set([o[1:] for o in order]) <= set(['']))
        cursor = self._sumycoll.objects.all()
        return list(cursor)


class TwseDualemaAlg(TwseAlgDBHandler):

    def __init__(self, **kwargs):
        self._alg = DualEMAAlgorithm
        super(TwseDualemaAlg, self).__init__(**kwargs)


class TwseBestTraderAlg(TwseAlgDBHandler):

    def __init__(self, **kwargs):
        self._alg = BestTraderAlgorithm
        super(TwseBestTraderAlg, self).__init__(**kwargs)


class TwseBBandsAlg(TwseAlgDBHandler):

    def __init__(self, **kwargs):
        self._alg = BBandsAlgorithm
        super(TwseBBandsAlg, self).__init__(**kwargs)


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

