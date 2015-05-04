# -*- coding: utf-8 -*-

import pandas as pd
import pytz
from collections import OrderedDict, defaultdict
from datetime import datetime

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.models import *
# use mongoengine(high level mongodb drive) as ORM data backend for Django access

__all__ = ['TwseHisDBHandler', 'OtcHisDBHandler']


class TwseHisDBHandler(object):

    def __init__(self, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._opt = kwargs.pop('opt', 'twse')
        db = 'twsehisdb' if not self._debug else 'testtwsehisdb'
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        twsehiscoll = switch(TwseHisColl, db)
        kwargs = []
        for i in range(3):
            kwargs.append({
                'coll': twsehiscoll,
                'debug': self._debug,
                'opt': self._opt
            })
        self._stock = TwseStockHisDBHandler(**kwargs[0])
        self._trader = TwseTraderHisDBHandler(**kwargs[1])
        self._credit = TwseCreditDBHandler(**kwargs[2])

    @property
    def stock(self):
        return self._stock

    @property
    def trader(self):
        return self._trader

    @property
    def credit(self):
        return self._credit

    def transform_all_data(self, starttime, endtime, stockids=[], traderids=[], orders=['totalvolume']*3, limit=10):
        """ transfrom stock/trader data as pandas panel """
        args = (starttime, endtime, stockids, orders[0], limit, self._stock.to_pandas)
        stockdt = self._stock.query_raw(*args)
        if self._debug:
            print stockdt
        args = (starttime, endtime, list(stockdt.keys()), traderids, 'stock', orders[1], limit, self._trader.to_pandas)
        traderdt = self._trader.query_raw(*args)
#        args = (starttime, endtime, stockids, orders[2], limit, self._stock.to_pandas)
#        stockdt = self._stock.query_raw(*args)
        return pd.concat([stockdt, traderdt], axis=2).fillna(0)


class OtcHisDBHandler(TwseHisDBHandler):

    def __init__(self, **kwargs):
        ckwargs = kwargs.copy()
        super(OtcHisDBHandler, self).__init__(**kwargs)
        self._debug = ckwargs.pop('debug', False)
        self._opt = ckwargs.pop('opt', 'otc')
        db = 'otchisdb' if not self._debug else 'testotchisdb'
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        otchiscoll = switch(OtcHisColl, db)
        kwargs = []
        for i in range(3):
            kwargs.append({
                'coll': otchiscoll,
                'debug': self._debug,
                'opt': self._opt
            })
        self._stock = OtcStockHisDBHandler(**kwargs[0])
        self._trader = OtcTraderHisDBHandler(**kwargs[1])
        self._credit = OtcCreditHisDBHandler(**kwargs[2])


class TwseStockHisDBHandler(object):

    def __init__(self, **kwargs):
        self._coll = kwargs.pop('coll', None)
        self._debug = kwargs.pop('debug', False)
        self._opt = kwargs.pop('opt', 'twse')
        db = 'stcokmapdb' if not self._debug else 'teststcokmapdb'
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        kwargs = {
            'debug': self._debug,
            'opt': self._opt
        }
        self._id = TwseIdDBHandler(**kwargs)
        self._mapcoll = switch(StockMapColl, db)
        self._ids = []

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids

    @property
    def coll(self):
        return self._coll

    @property
    def mapcoll(self):
        return self._mapcoll

    def update_raw(self, item):
        pass

    def delete_raw(self, item):
        pass

    def insert_raw(self, item):
        keys = [k for k,v in StockData._fields.iteritems()]
        for it in item:
            data = {k:v for k, v in it.items() if k in keys}
            data = StockData(**data)
            cursor = self._coll.objects(Q(date=it['date']) & Q(stockid=it['stockid']))
            cursor = list(cursor)
            coll = self._coll() if len(cursor) == 0 else cursor[0]
            coll.stockid = it['stockid']
            coll.date = it['date']
            coll.data = data
            coll.save()

    def query_raw(self, starttime, endtime, stockids=[], order='totalvolume', limit=10, callback=None):
        """ return orm
        <stockid>                               | <stockid> ...
                    open| high| low|close|volume|          | open | ...
        20140928    100 | 101 | 99 | 100 | 100  | 20140928 | 11   | ...
        20140929    100 | 102 | 98 | 99  | 99   | 20140929 | 11   | ...
        """
        map_f = """
            function () {
                try {
                    var key =  { stockid : this.stockid };
                    var diff = this.data.high - this.data.low;
                    var value = {
                        totalvolume: this.data.volume,
                        totaldiff: diff,
                        data: [{
                            date: this.date,
                            open: this.data.open,
                            high: this.data.high,
                            low: this.data.low,
                            close: this.data.close,
                            price: this.data.close,
                            volume: this.data.volume
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
                    totalvolume: 0,
                    totaldiff: 0,
                    data: []
                };
                if (values.length == 0) {
                    return redval;
                }
                for (var i=0; i < values.length; i++) {
                    redval.totalvolume += values[i].totalvolume;
                    redval.totaldiff += values[i].totaldiff;
                    redval.data = values[i].data.concat(redval.data);
                }
                return redval;
            }
        """
        decorder = ['totalvolume', 'totaldiff', 'maxhigh']
        incorder = ['minlow', 'minhigh']
        bufwin = endtime - starttime
        assert(order in decorder + incorder)
        cursor = self._coll.objects(Q(date__gte=starttime) & Q(date__lte=endtime) & Q(stockid__in=stockids))
        results = cursor.map_reduce(map_f, reduce_f, 'stockmap')
        results = list(results)
        pool = sorted(results, key=lambda x: x.value[order], reverse=True if order in decorder else False)[:limit]
        retval = []
        for it in pool:
            coll = { 'datalist': [] }
            for data in sorted(it.value['data'], key=lambda x: x['date']):
                coll['datalist'].append(data)
            coll.update({
                # key
                'date': endtime,
                'bufwin': bufwin.days,
                'stockid': it.key['stockid'],
                'order': order,
                'stocknm': self._id.stock.get_name(it.key['stockid']),
                # value
                'totalvolume': it.value['totalvolume'],
                'totaldiff': it.value['totaldiff']
            })
            retval.append(coll)
        return callback(retval) if callback else retval

    def to_pandas(self, cursor):
        item = OrderedDict()
        for it in cursor:
            index, data = [], []
            for i in it['datalist']:
                date = i.pop('date', None)
                if date:
                    index.append(pytz.timezone('UTC').localize(date))
                    data.append(i)
            if index and data:
                id = it['stockid']
                item.update({id: pd.DataFrame(data, index=index).fillna(0)})
        return pd.Panel(item)

    def to_map(self, cursor):
        keys = [k for k,v in StockMapColl._fields.iteritems()]
        for it in cursor:
            cursor = self._mapcoll.objects(Q(date=it['date']) & Q(buf_win=it['bufwin']) & Q(stockid=it['stockid']) & Q(order=it['order']))
            cursor = list(cursor)
            coll = self._coll() if len(cursor) == 0 else cursor[0]
            [setattr(coll, "%s" %(k), it[k]) for k in keys]
            coll.save()

    def query_map(self,):
        pass

    def delete_map(self,):
        pass

class TwseTraderHisDBHandler(object):

    def __init__(self, **kwargs):
        self._coll = kwargs['coll']
        self._debug = kwargs['debug']
        self._opt = kwargs['opt']
        host, port = MongoDBDriver._host, MongoDBDriver._port
        db = 'tradermapdb' if not self._debug else 'testtradermapdb'
        connect(db, host=host, port=port, alias=db)
        self._mapcoll = switch(TraderMapColl, db)
        kwargs = {
            'debug': self._debug,
            'opt': self._opt
        }
        self._id = TwseIdDBHandler(**kwargs)
        self._cache = []
        self._ids = []

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids

    @property
    def coll(self):
        return self._coll

    @property
    def mapcoll(self):
        return self._mapcoll

    def update_raw(self, item):
        pass

    def delete_raw(self, item):
        pass

    def insert_raw(self, item):
        keys = [k for k,v in TraderData._fields.iteritems()]
        toplist = []
        for it in item['toplist']:
            data = {k:v for k, v in it['data'].items() if k in keys}
            info = {
                'traderid': it['traderid'],
                'data': TraderData(**data)
            }
            toplist.append(TraderInfo(**info))
        cursor = self._coll.objects(Q(date=item['date']) & Q(stockid=item['stockid']))
        cursor = list(cursor)
        coll = self._coll() if len(cursor) == 0 else cursor[0]
        coll.stockid = item['stockid']
        coll.date = item['date']
        coll.toplist = toplist
        coll.save()

    def query_raw(self, starttime, endtime, stockids=[], traderids=[],
            base='stock', order='totalvolume', limit=10, callback=None):
        """ get rank toplist volume stock/trader data
            <stockid>                                          <stockid>
                     | top0_v/p_<traderid>| top1  | ... top10 |          | top0_<traderid>
            20140928 |  100               |   30  |           | 20140928 | ...
            20140929 |    0               |   20  |           | 20140929 | ...
            -------------------------------------------------------------------------
                        100                   50

            <traderid>                                    <traderid>
                     | top0_<stockid> | top1  | ... top10 |          | top0_<traderid>
            20140928 |  100           |   30  |           | 20140928 | ...
            20140929 |    0           |   20  |           | 20140929 | ...
            -------------------------------------------------------------------------
                        100                   50
        """
        map_f = """
            function () {
                try {
                    for (var i=0; i < this.toplist.length; i++) {
                        var key =  { traderid: this.toplist[i].traderid, stockid: this.stockid };
                        var totalvolume = this.toplist[i].data.totalvolume;
                        var buyvolume = this.toplist[i].data.buyvolume;
                        var sellvolume = this.toplist[i].data.sellvolume;
                        var avgbuyprice = this.toplist[i].data.avgbuyprice;
                        var avgsellprice = this.toplist[i].data.avgsellprice;
                        var hit = 0;
                        var ratio = 0;
                        var tradeprice = 0;
                        var tradevolume = 0;
                        var maxvolume = Math.max(buyvolume, sellvolume);
                        var minvolume = Math.min(buyvolume, sellvolume);
                        var maxprice = Math.max(avgbuyprice, avgsellprice);
                        var minprice = Math.min(avgbuyprice, avgsellprice);
                        if (this.data.volume >0) {
                            if (maxvolume >0) {
                                ratio = maxvolume / this.data.volume * 100;
                                hit = 1;
                            }
                        }
                        if (minprice > 0 && minvolume > 0) {
                            tradeprice = maxprice - minprice;
                            tradevolume = minvolume;
                        }
                        var value = {
                            totalvolume: totalvolume,
                            totalbuyvolume: buyvolume,
                            totalsellvolume: sellvolume,
                            totalhit: hit,
                            totaltradeprice: tradeprice,
                            totaltradevolume: tradevolume,
                            data: [{ date: this.date, ratio: ratio, avgbuyprice: avgbuyprice, avgsellprice: avgsellprice, buyvolume: buyvolume, sellvolume: sellvolume }]
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
                    totalvolume: 0,
                    totalbuyvolume: 0,
                    totalsellvolume: 0,
                    totalhit: 0,
                    totaltradeprice: 0,
                    totaltradevolume: 0,
                    data: []
                };
                if (values.length == 0) {
                    return redval;
                }
                for (var i=0; i < values.length; i++) {
                    redval.totalvolume += values[i].totalvolume;
                    redval.totalbuyvolume += values[i].totalbuyvolume;
                    redval.totalsellvolume += values[i].totalsellvolume;
                    redval.totalhit += values[i].totalhit;
                    redval.totaltradeprice += values[i].totaltradeprice;
                    redval.totaltradevolume += values[i].totaltradevolume;
                    redval.data = values[i].data.concat(redval.data);
                }
                return redval;
            }
        """
        ids = stockids if base == 'stock' else traderids
        mkey = 'stockid' if base == 'stock' else 'traderid'
        bufwin = endtime - starttime
        decorder = ['totalvolume', 'totalhit', 'totalbuyvolume', 'totalsellvolume', 'totaltradeprice', 'totaltradevolume']
        incorder = []
        assert(order in decorder + incorder)
        if stockids and traderids:
            cursor = self._coll.objects(
                Q(date__gte=starttime) & Q(date__lte=endtime) &
                (Q(stockid__in=stockids) & Q(toplist__traderid__in=traderids)))
        else:
            cursor = self._coll.objects(
                Q(date__gte=starttime) & Q(date__lte=endtime) &
                (Q(stockid__in=stockids) | Q(toplist__traderid__in=traderids)))
        results = cursor.map_reduce(map_f, reduce_f, 'toptradermap')
        results = list(results)
        retval = []
        pool = sorted(results, key=lambda x: x.value[order], reverse=True if order in decorder else False)[:limit]
        for i, it in enumerate(pool):
             coll = { 'datalist': [] }
             for data in sorted(it.value['data'], key=lambda x: x['date']):
                 coll['datalist'].append(data)
             coll.update({
                 # html link
                 'opt': 'twse' if self.__class__.__name__ == 'TwseTraderHisDBHandler' else 'otc',
                 'starttime': datetime.strftime(starttime, "%Y%m%d"),
                 'endtime': datetime.strftime(endtime, "%Y%m%d"),
                 # key
                 'date': endtime,
                 'bufwin': bufwin.days,
                 'traderid': it.key['traderid'],
                 'stockid': it.key['stockid'],
                 'order': order,
                 'tradernm': self._id.trader.get_name(it.key['traderid']),
                 'stocknm': self._id.stock.get_name(it.key['stockid']),
                 # value
                 'totalvolume': it.value['totalvolume'],
                 'totalbuyvolume': it.value['totalbuyvolume'],
                 'totalsellvolume': it.value['totalsellvolume'],
                 'totalhit': it.value['totalhit'],
                 'totaltradeprice': it.value['totaltradeprice'],
                 'totaltradevolume': it.value['totaltradevolume'],
                 'alias': "top%d" % (i)
             })
             retval.append(coll)
        self._cache = retval
        return callback(retval) if callback else retval

    def to_pandas(self, cursor, base='stock'):
        item = OrderedDict()
        ids = [it['stockid'] if base =='stock' else it['traderid'] for it in cursor]
        for id in ids:
            df = pd.DataFrame()
            pool = list(filter(lambda x: x['stockid']==id, cursor)) if base == 'stock' else list(filter(lambda x: x['traderid']==id, cursor))
            for it in pool:
                index, data= [], []
                for i in it['datalist']:
                    date = i.pop('date', None)
                    if date:
                        index.append(pytz.timezone('UTC').localize(date))
                        mdata = {
                            "%s_ratio" % (it['alias']): i['ratio'],
                            "%s_avgbuyprice" % (it['alias']): i['avgbuyprice'],
                            "%s_avgsellprice" % (it['alias']): i['avgsellprice'],
                            "%s_buyvolume" % (it['alias']): i['buyvolume'],
                            "%s_sellvolume" % (it['alias']): i['sellvolume']
                        }
                        data.append(mdata)
                if index and data:
                    df = pd.concat([df, pd.DataFrame(data, index=index).fillna(0)], axis=1)
                    item.update({id: df})
        return pd.Panel(item)

    def get_alias(self, ids=[], base='stock', aliases=['top0']):
        """ get alias map as virtual to physical map """
        pool = list(filter(lambda x: x['alias'] in aliases, self._cache))
        for it in aliases:
            for i in pool:
                if i['alias'] == it:
                    yield i['stockid'] if base == 'stock' else i['traderid']

    def to_map(self, cursor):
        keys = [k for k,v in TraderMapColl._fields.iteritems()]
        for it in cursor:
            cursor = self._mapcoll.objects(Q(date=it['date']) & Q(buf_win=it['bufwin']) & Q(stockid=it['stockid']) & Q(order=it['traderid']) & Q(order=it['order']))
            cursor = list(cursor)
            coll = self._coll() if len(cursor) == 0 else cursor[0]
            [setattr(coll, "%s" %(k), it[k]) for k in keys]
            coll.save()

    def query_map(self, ):
        pass

    def delete_map(self,):
        pass

class TwseCreditDBHandler(object):

    def __init__(self, **kwargs):
        self._coll = kwargs.pop('coll', None)
        self._debug = kwargs.pop('debug', False)
        self._opt = kwargs.pop('opt', 'twse')
        host, port = MongoDBDriver._host, MongoDBDriver._port
        db = 'creditmapdb' if not self._debug else 'testcreditmapdb'
        connect(db, host=host, port=port, alias=db)
        kwargs = {
            'debug': self._debug,
            'opt': self._opt
        }
        self._id = TwseIdDBHandler(**kwargs)
        self._mapcoll = switch(CreditMapColl, db)
        self._ids = []

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids

    def update_raw(self, item):
        pass

    def delete_raw(self, item):
        pass

    def insert_raw(self, item):
        keys = [k for k,v in CreditData._fields.iteritems()]
        for it in item:
            data = {k:v for k, v in it.items() if k in keys}
            data = CreditData(**data)
            cursor = self._coll.objects(Q(date=it['date']) & Q(stockid=it['stockid']))
            cursor = list(cursor)
            coll = self._coll() if len(cursor) == 0 else cursor[0]
            coll.stockid = it['stockid']
            coll.date = it['date']
            if it['type'] == 'finance':
                coll.finance = data
            if it['type'] == 'bearish':
                coll.bearish = data
            coll.save()

    def query_raw(self, starttime, endtime, stockids=[], order='totalvolume', limit=10, callback=None):
        """ return orm
        <stockid>                                                | <stockid> ...
                    finance_buy| finance_sely| finance_limit| ...|
        20140928    100        | 101         |          999 | ...|
        20140929    100        | 102         |          999 | ...|
        """
        map_f = """
            function () {
                try {
                    var key =  { stockid : this.stockid };
                    var value = {
                        finance_trend = (this.finance.curremain - this.finance.preremain) / this.finance.preremain
                        finance_used = this.finance.curremain / this.finance.limit * 100
                        bearish_trend = (this.bearish.curremain - this.bearish.preremain) / this.bearish.preremain
                        bearish_used = this.bearish.curremain / this.bearish.limit * 100
                        data: [{
                            finance_buyvolume = this.finance.buyvolume,
                            finance_sellvolume = this.finance.sellvolume,
                            finance_used = finance_used,
                            bearish_buyvolume = this.bearish.buyvolume,
                            bearish_sellvolume = this.bearish.sellvolume,
                            bearish_used = bearish_used
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
                    finance_trend: 0,
                    bearish_trend: 0,
                    data: []
                };
                if (values.length) == 0) {
                    return redval;
                }
                for (var i=0; i < values.length; i++) {
                    redval.finance_trend += values[i].finance_trend;
                    redval.bearish_trend += values[i].bearish_trend;
                    redval.data = values[i].data.concat(redval.data);
                }
                return redval;
            }
        """
        decorder = ['incfinance', 'incbearish', 'totalvolume']
        incorder = ['decfinance', 'decbearish']
        bufwin = endtime - starttime
        assert(order in decorder + incorder)
        cursor = self._coll.objects(Q(date__gte=starttime) & Q(date__lte=endtime) & Q(stockid__in=stockids))
        results = cursor.map_reduce(map_f, reduce_f, 'creditmap')
        results = list(results)
        pool = sorted(results, key=lambda x: x.value[order], reverse=True if order in decorder else False)[:limit]
        retval = []
        for it in pool:
            coll = { 'datalist': [] }
            for data in sorted(it.value['data'], key=lambda x: x['date']):
                coll['datalist'].append(data)
            coll.update({
                'stockid': it.key['stockid'],
                'bufwin': bufwin.days,
                'order': order
            })
            retval.append(coll)
        return callback(retval) if callback else retval

    def to_pandas(self, cursor):
        item = OrderedDict()
        for it in cursor:
            index, data = [], []
            for i in it['datalist']:
                date = i.pop('date', None)
                if date:
                    index.append(pytz.timezone('UTC').localize(date))
                    data.append(i)
            if index and data:
                id = it['stockid']
                item.update({id: pd.DataFrame(data, index=index).fillna(0)})
        return pd.Panel(item)

    def to_map(self, cursor):
        pass

    def query_map(self, **kwargs):
        pass

    def delete_map(self, item):
        pass

class OtcStockHisDBHandler(TwseStockHisDBHandler):
    def __init__(self, **kwargs):
        ckwargs = kwargs.copy()
        super(OtcStockHisDBHandler, self).__init__(**kwargs)
        self._id = OtcIdDBHandler(**ckwargs)

class OtcTraderHisDBHandler(TwseTraderHisDBHandler):
    def __init__(self, **kwargs):
        ckwargs = kwargs.copy()
        super(OtcTraderHisDBHandler, self).__init__(**kwargs)
        self._id = OtcIdDBHandler(**ckwargs)

class OtcCreditHisDBHandler(TwseCreditDBHandler):
    def __init__(self, **kwargs):
        ckwargs = kwargs.copy()
        super(OtcCreditHisDBHandler, self).__init__(**kwargs)
        self._id = OtcIdDBHandler(**ckwargs)
