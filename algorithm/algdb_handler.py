# -*- coding: utf-8 -*-

import copy
import json 
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

class TwseAlgDBHandler(object):

    def __init__(self, alg, **kwargs):
        self._alg = alg
        self._order = kwargs.pop('order', [])
        self._cfg = kwargs.pop('cfg', {})
        self._reserved = kwargs.pop('reserved', False)
        self._debug = kwargs.pop('debug', False)
        # hisframe collect args
        self._kwargs = {
            'opt': kwargs.pop('opt', None),
            'starttime': kwargs.pop('starttime', datetime.utcnow() - timedelta(days=30)),
            'endtime': kwargs.pop('endtime', datetime.utcnow()),
            'targets': ['stock'],
            'base': kwargs.pop('base', 'stock'),
            'stockids': kwargs.pop('stockids', []),
            'traderids': kwargs.pop('traderids', []),
            'limit': kwargs.pop('limit', 10),
            'debug': self._debug
        }
        db = "twsealgdb"
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._algcoll = switch(AlgStrategyColl, db)
        self._id = TwseIdDBHandler(debug=self._debug, opt='twse')
        self._report = Report(alg, sort=[('buys', False), ('sells', False), ('portfolio_value', False)], limit=100)

    @property
    def algcoll(self):
        return self._algcoll

    def iter_hisframe(self):
        if not self._reserved:
            stockids = self._kwargs['stockids']
            for stockid in stockids:
                self._kwargs.update({'stockids': [stockid]})
                panel, handler = collect_hisframe(**copy.deepcopy(self._kwargs))
                yield stockid, panel, handler
        else:
            panel, handler = collect_hisframe(**copy.deepcopy(self._kwargs))
            yield stockid, panel, handler 

    def run(self):
        for stockid, panel, dbhandler in self.iter_hisframe():
            if not panel.empty and dbhandler:
                sim_params = SimulationParameters(
                    period_start=panel[stockid].index[0],
                    period_end=panel[stockid].index[-1],
                    data_frequency='daily',
                    emission_rate='daily')
                alg = self._alg(dbhandler, **self._cfg)
                self._cfg = alg.cfg
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

    def delete_summary(self, uid):
        pass

    def insert_summary(self, df):
        keys = [k for k,v in AlgSummaryColl._fields.iteritems() if k not in ['id', '_cls']]
        toplist = []
        names = df.columns.values.tolist()
        algnm = self._alg.__name__.lower()
        cfg = json.dumps(dict(self._cfg))
        date = self._kwargs['endtime']
        for k, v in df.T.to_dict().items():
            data = { 'stockid': k }
            data.update(v)
            toplist.append(AlgSummaryColl(**data))
        cursor = self._algcoll.objects(Q(algnm=algnm) & Q(cfg=cfg) & Q(date=date))
        cursor = list(cursor)
        coll = self._algcoll() if len(cursor) == 0 else cursor[0]
        coll.cfg = cfg
        coll.algnm = algnm
        coll.date = date
        coll.toplist = toplist
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
                    for(var i=0; i < this.toplist.length; i++) {
                        var key =  { algnm: this.algnm, cfg: this.cfg, stockid: this.toplist[i].stockid };
                        var portfolio = this.toplist[i].portfolio_value;
                        var buys = this.toplist[i].buys;
                        var sells = this.toplist[i].sells;
                        var used = this.toplist[i].capital_used;
                        var alpha = this.toplist[i].alpha;
                        var beta = this.toplist[i].beta;
                        var sharpe = this.toplist[i].sharpe;
                        var max_drawdown = this.toplist[i].max_drawdown;
                        var benchmark = this.toplist[i].benchmark_period_return;
                        // as constraint/sort key
                        var value = {
                            portfolio: portfolio,
                            buys: buys,
                            sells: sells,
                            used: used,
                            alpha: alpha,
                            beta: beta,
                            sharpe: sharpe,
                            max_drawdown: max_drawdown,
                            benchmark: benchmark
                        };
                        emit(key, value);
                    }
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
                    portfolio: 0,
                    buys: 0,
                    sells: 0,
                    used: 0,
                    alpha: 0,
                    beta: 0,
                    sharpe: 0,
                    max_drawdown: 0,
                    benchmark: 0
                };
                if (values.length == 1) {
                    redval.portfolio = values[0].portfolio;
                    redval.buys = values[0].buys;
                    redval.sells = values[0].sells;
                    redval.used = values[0].used;
                    redval.alpha = values[0].alpha;
                    redval.beta = values[0].beta;
                    redval.sharpe = values[0].sharpe; 
                    redval.max_drawdown = values[0].max_drawdown;
                    redval.benchmark = values[0].benchmark;
                }
                return redval;
            }
        """
        finalize_f = """
        """
        bufwin = (endtime - starttime).days
        cursor = self._algcoll.objects(Q(date__gte=starttime) & Q(date__lte=endtime)).order_by('-date').limit(1)
        results = list(cursor.map_reduce(map_f, reduce_f, 'algmap'))
        if constraint:
            results = filter(constraint, results)
        if order:
            results = sorted(results, key=order)[:limit]
        retval = []
        for it in results:
            coll = {
                # key
                'algnm': it.key['algnm'],
                'stockid': it.key['stockid'],
                'stocknm': self._id.stock.get_name(it.key['stockid']),
                'cfg': it.key['cfg'],
                'endtime': endtime, 
                # value
                'portfolio': it.value['portfolio'],
                'buys': it.value['buys'],
                'sells': it.value['sells'],
                'used': it.value['used'],
                'alpha': it.value['alpha'],
                'beta': it.value['beta'],
                'sharpe': it.value['sharpe'],
                'max_drawdown': it.value['max_drawdown'],
                'benchmark': it.value['benchmark']
            }
            retval.append(coll)
        return callback(retval) if callback else retval

    def to_pandas(self):
        pass


class OtcAlgDBHandler(TwseAlgDBHandler):

    def __init__(self, alg, **kwargs):
        super(OtcAlgDBHandler, self).__init__(alg, **kwargs)
        db = "otcalgdb"
        db = db if not self._debug else 'test' + db
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        self._sumycoll = switch(AlgSummaryColl, db)
        self._id = OtcIdDBHandler(debug=self._debug, opt='otc')
