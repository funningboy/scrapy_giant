# -*- coding: utf-8 -*-

import pandas as pd
import pytz
import copy
from collections import OrderedDict
from datetime import datetime, timedelta

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.collects import create_hiscollect
from handler.tasks import collect_hisframe, iddb_tasks
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

    def __init__(self, **kwargs):
        self._debug = kwargs.get('debug', False)
        self._cfg = kwargs.pop('cfg', {})
        assert(self._alg)
        db = "twse%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._collect = create_hiscollect(**kwargs)
        self._report = Report(sort=[('buys', False), ('sells', False), ('portfolio_value', False)], limit=100)
        self._id = iddb_tasks['twse'](debug=self._debug)

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
            data, handler = collect_hisframe(copy.deepcopy(self._collect))
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
        keys = [k for k,v in AlgSummaryColl._fields.iteritems() if k not in ['id']]
        names = df.columns.values.tolist()
        for ix, cols in df.iterrows():
            cursor = self._sumycoll.objects(Q(date=cols['date']) &Q(bufwin=cols['bufwin']) & Q(stockid=ix))
            coll = self._sumycoll() if len(cursor) == 0 else cursor[0]
            [setattr(coll, k, cols[k]) for k in names if k in keys]
            coll.stockid = ix
            coll.save()

    def to_detail(self, df):
        retval = []
        keys = [k for k,v in AlgDetailColl._fields.iteritems()]
        names = df.columns.values.tolist()
        for ix, cols in df.iterrows():
            coll = {k:cols[k] for k in names if k in keys}
            coll.update({'date': ix})
            retval.append(coll)
        return retval

    def query_summary(self, watchtime=datetime.utcnow(), stockids=[], order=['-totalportfolio'], limit=10, callback=None):
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
                    var value = {
                        totalportfolio: this.portfolio_value,
                        totalbuys: this.buys,
                        totalsells: this.sells,
                        totalused: this.capital_used,
                        data: [{
                            bufwin: this.bufwin
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
                if (values.length == 0) {
                    return redval;
                }
                for (var i=0; i < values.length; i++) {
                    redval.totalportfolio += values[i].totalportfolio;
                    redval.totalbuys += values[i].totalbuys;
                    redval.totalsells += values[i].totalsells;
                    redval.totalused += values[i].tottalused;
                    redval.data = values[i].data.concat(redval.data);
                }
                return redval;
            }
        """
        finalize_f = """
        """
        assert(set([o[1:] for o in order]) <= set(['totalbuys', 'totalsells', 'totalportfolio', 'totalused']))
        starttime, endtime = watchtime - timedelta(3), watchtime
        if stockids:
            cursor = self._sumycoll.objects(Q(date__gte=starttime) & Q(date__lte=endtime)) & (Q(stockid__in=stockids))
        else:
            cursor = self._sumycoll.objects(Q(date__gte=starttime) & Q(date__lte=endtime))
        results = cursor.map_reduce(map_f, reduce_f, 'algmap')
        results = list(results)
        reorder = lambda k: map(lambda x: k.value[x[1:]] if x.startswith('+') else -k.value[x[1:]], order)
        pool = sorted(results, key=reorder)[:limit]
        retval = []
        for it in pool:
            coll = {
                # key
                'watchtime': watchtime,
                'stockid': it.key['stockid'],
                'order': order,
                'stocknm': self._id.stock.get_name(it.key['stockid']),
                # value
                'totalportfolio': it.value['totalportfolio'],
                'totalbuys': it.value['totalbuys'],
                'totalsells': it.value['totalsells'],
                'tottalused': it.value['totalused']
            }
            retval.append(coll)
        return callback(retval) if callback else retval


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
        super(OtcDualemaAlg, self).__init__(**copy.deep(kwargs))
        db = "otc%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._id = iddb_tasks['otc'](debug=self._debug)

class OtcBestTraderAlg(TwseBestTraderAlg):

    def __init__(self, **kwargs):
        super(OtcBestTraderAlg, self).__init__(**copy.deep(kwargs))
        db = "otc%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._id = iddb_tasks['otc'](debug=self._debug)

class OtcBBandsAlg(TwseBBandsAlg):

    def __init__(self, **kwargs):
        super(OtcBBandsAlg, self).__init__(**copy.deep(kwargs))
        db = "otc%s" %(algdbmap[self._alg])
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._id = iddb_tasks['otc'](debug=self._debug)
