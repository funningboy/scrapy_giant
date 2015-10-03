# -*- coding: utf-8 -*-

import copy
from collections import OrderedDict
from datetime import datetime, timedelta

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.tasks import *
from itertools import product
from zipline.finance.trading import SimulationParameters

from algorithm.models import *
from algorithm.report import Report
from algorithm.dualema import DualEMAAlgorithm
from algorithm.besttrader import BestTraderAlgorithm
from algorithm.bbands import BBandsAlgorithm
from algorithm.randforest import RandForestAlgorithm
from algorithm.kmeans import KmeansAlgorithm
#from algorithm.kdtree import KdtKnnAlgorithm


# register all alg to algdb_handler via decorator
algclass = lambda x: x[0]+x[1]

__all__ = map(algclass, list(product(
        ('Twse', 'Otc'), 
        ('DualemaAlg', 'BestTraderAlg', 'BBandsAlg', 'RandForestAlg')
    )))

# alg db map
algdbmap = {
    DualEMAAlgorithm: 'dualemadb',
    BestTraderAlgorithm: 'btraderdb',
    BBandsAlgorithm: 'bbandsdb',
    RandForestAlgorithm: 'rforestdb',
    KmeansAlgorithm: 'kmeansdb'
}

class TwseAlgDBHandler(object):

    def __init__(self, **kwargs):
        self._order = kwargs.pop('order', [])
        self._cfg = kwargs.pop('cfg', {})
        self._debug = kwargs.pop('debug', False)
        self._kwargs = {
            'opt': kwargs.pop('opt', None),
            'starttime': kwargs.pop('starttime', datetime.utcnow() - timedelta(days=30)),
            'endtime': kwargs.pop('endtime', datetime.utcnow()),
            'base': kwargs.pop('base', 'stock'),
            'stockids': kwargs.pop('stockids', []),
            'traderids': kwargs.pop('traderids', []),
            'limit': kwargs.pop('limit', 10),
            'debug': self._debug
        }
        db = "twse%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._id = TwseIdDBHandler(debug=self._debug, opt='twse')
        self._report = Report(sort=[('buys', False), ('sells', False), ('portfolio_value', False)], limit=100)

    @property
    def sumycoll(self):
        return self._sumycoll

    def iter_hisframe(self):
        stockids = self._kwargs['stockids']
        for stockid in stockids:
            self._kwargs.update({'stockids': [stockid]})
            panel, handler = collect_hisframe(**copy.deepcopy(self._kwargs))
            yield stockid, panel, handler

    def run(self):
        for stockid, panel, dbhandler in self.iter_hisframe():
            if not panel.empty and dbhandler:
                sim_params = SimulationParameters(
                    period_start=panel[stockid].index[0],
                    period_end=panel[stockid].index[-1],
                    data_frequency='daily',
                    emission_rate='daily'
                )
                alg = self._alg(dbhandler, **self._cfg)
                results = alg.run(panel).fillna(0)
                risks = alg.perf_tracker.handle_simulation_end()
                self._report.collect("%s" %(stockid), results, risks)

    def finalize(self, callback=None):
        df = self._report.summary()
        if callback == self.to_detail:
            return callback(df)
        if callback == self.insert_summary:
            return callback(df)
        return df

    def delete_summary(self, item):
        pass

    def insert_summary(self, df):
        keys = [k for k,v in AlgSummaryColl._fields.iteritems() if k not in ['id', '_cls']]
        names = df.columns.values.tolist()
        for ix, cols in df.iterrows():
            cursor = self._sumycoll.objects(Q(date=cols['date']) & Q(stockid=ix))
            coll = self._sumycoll() if len(cursor) == 0 else cursor[0]
            [setattr(coll, k, cols[k]) for k in names if k in keys]
            coll.stockid = ix
            coll.save()

    def to_detail(self, df):
        retval = []
        stockids = df.T.to_dict().keys()
        keys = [k for k,v in AlgDetailColl._fields.iteritems() if k not in ['id', '_cls']]
        for stockid in stockids:
            df = self._report.iter_report(stockid)    
            names = df.columns.values.tolist()
            for ix, cols in df.iterrows():
                coll = {k:cols[k] for k in names if k in keys}
                coll.update({
                    'date': ix,
                    'stockid': stockid
                    })
                retval.append(coll)
        return retval

    def query_summary(self, starttime, endtime, cfg, constraint=None, order=None, limit=10, callback=None):
        """ return orm
        <algorithm>
        <watchtime> |<bufwin> | <stockid> | <traderid> | buys | sells ...
        20140928    |  5      |  2330     |   null     | 100  | 100
        20140929    | 10      |  2317     |  1440      | 99   | 99
        """
        map_f = """
            function () {
                try {
                    var key =  { stockid : this.stockid };
                    // as constraint/sort key
                    var value = {
                        totalportfolio: this.portfolio_value,
                        totalbuys: this.buys,
                        totalsells: this.sells,
                        totalused: this.capital_used,
                        data: [{
                            date: this.date,
                            buy: this.buys,
                            sell: this.sells,
                            portfolio: this.portfolio_value,
                            used: this.capital_used
                        }]
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
            function (key, values) {
                var redval = {
                    totalportfolio: 0,
                    totalbuys: 0,
                    totalsells: 0,
                    totalused: 0,
                    data: []
                };
                for (var i=0; i < values.length; i++) {
                    redval.totalportfolio += values[i].totalportfolio;
                    redval.totalbuys += values[i].totalbuys;
                    redval.totalsells += values[i].totalsells;
                    redval.totalused += values[i].totalused;
                    redval.data = values[i].data.concat(redval.data);
                }
                return redval;
            }
        """
        finalize_f = """
        """
        bufwin = (endtime - starttime).days
        cursor = self._sumycoll.objects(Q(date__gte=starttime) & Q(date__lte=endtime))
        results = list(cursor.map_reduce(map_f, reduce_f, 'algmap'))
        if constraint:
            results = filter(constraint, results)
        if order:
            results = sorted(results, key=order)[:limit]
        retval = []
        for it in results:
            coll = {
                # key
                'watchtime': endtime,
                'bufwin': bufwin,
                'stockid': it.key['stockid'],
                'stocknm': self._id.stock.get_name(it.key['stockid']),
                # value
                'totalportfolio': it.value['totalportfolio'],
                'totalbuys': it.value['totalbuys'],
                'totalsells': it.value['totalsells'],
                'totalused': it.value['totalused']
            }
            retval.append(coll)
        return callback(retval) if callback else retval

    def to_pandas(self):
        pass


class TwseDualemaAlg(TwseAlgDBHandler):

    def __init__(self, **kwargs):
        self._alg = DualEMAAlgorithm
        super(TwseDualemaAlg, self).__init__(**kwargs)
        self._kwargs.update({'targets': ['stock']})

class TwseBestTraderAlg(TwseAlgDBHandler):

    def __init__(self, **kwargs):
        self._alg = BestTraderAlgorithm
        super(TwseBestTraderAlg, self).__init__(**kwargs)
        self._kwargs.update({'targets': ['stock', 'trader']})

class TwseBBandsAlg(TwseAlgDBHandler):

    def __init__(self, **kwargs):
        self._alg = BBandsAlgorithm
        super(TwseBBandsAlg, self).__init__(**kwargs)
        self._kwargs.update({'targets': ['stock']})

class TwseRandForestAlg(TwseAlgDBHandler):

    def __init__(self, **kwargs):
        self._alg = RandForestAlgorithm
        super(TwseRandForestAlg, self).__init__(**kwargs)
        self._kwargs.update({'targets': ['stock']})

class OtcDualemaAlg(TwseDualemaAlg):

    def __init__(self, **kwargs):
        super(OtcDualemaAlg, self).__init__(**kwargs)
        db = "otc%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._id = OtcIdDBHandler(debug=self._debug, opt='otc')

class OtcBestTraderAlg(TwseBestTraderAlg):

    def __init__(self, **kwargs):
        super(OtcBestTraderAlg, self).__init__(**kwargs)
        db = "otc%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._id = OtcIdDBHandler(debug=self._debug, opt='otc')

class OtcBBandsAlg(TwseBBandsAlg):

    def __init__(self, **kwargs):
        super(OtcBBandsAlg, self).__init__(**kwargs)
        db = "otc%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._id = OtcIdDBHandler(debug=self._debug, opt='otc')

class OtcRandForestAlg(TwseRandForestAlg):

    def __init__(self, **kwargs):
        super(OtcRandForestAlg, self).__init__(**kwargs)
        db = "otc%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._id = OtcIdDBHandler(debug=self._debug, opt='otc')