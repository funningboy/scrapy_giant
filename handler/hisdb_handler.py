# -*- coding: utf-8 -*-

import pandas as pd
import json
from bson import json_util
import pytz
import copy
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.models import *
# use mongoengine(high level mongodb drive) as ORM data backend for Django access

__all__ = ['TwseHisDBHandler', 'OtcHisDBHandler']


class TwseHisDBHandler(object):
    """
    >>> starttime = datetime.utcnow() - timedelta(days=10)
    >>> endtime = datetime.utcnow()
    >>> dbhandler = TwseHisDBHandler(debug=True, opt='twse')
    >>> dbhandler.stock.ids = ['2317']
    >>> args = (starttime, endtime, [stockid], 'stock', ['-totalvolume'], 10)
    >>> cursor = dbhandler.stock.query_raw(*args)
    >>> data = dbhandler.stock.to_pandas(cursor)
    >>> print data
    >>> dbhandler.trader.ids = ['2317']
    >>> args = (starttime, endtime, ['2317'], ['1440'], 'stock', ['-totalvolume'], 10)
    >>> cursor = dbhandler.trader.query_raw(*args)
    >>> data = dbhandler.trader.to_pandas(cursor)
    >>> print data
    >>> args = (starttime, endtime, [stockid], 'stock', ['-financeused'], 10)
    >>> cursor = dbhandler.credit.query_raw(*args)
    >>> data = dbhandler.credit.to_pandas(cursor)
    >>> print data
    """
    def __init__(self, **kwargs):
        self._debug = kwargs.pop('debug', False)
        db = 'twsehisdb' if not self._debug else 'testtwsehisdb'
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        twsehiscoll = switch(TwseHisColl, db)
        kwargs = {
            'stock': {
                'coll': twsehiscoll,
                'debug': self._debug
            },
            'trader': {
                'coll': twsehiscoll,
                'debug': self._debug
            },
            'credit': {
                'coll': twsehiscoll,
                'debug': self._debug
            },
            'future': {
                'coll': twsehiscoll,
                'debug': self._debug
            }
        }
        self._stock = TwseStockHisDBHandler(**kwargs['stock'])
        self._trader = TwseTraderHisDBHandler(**kwargs['trader'])
        self._credit = TwseCreditHisDBHandler(**kwargs['credit'])
        self._future = TwseFutureHisDBHandler(**kwargs['future'])

    @property
    def stock(self):
        return self._stock

    @property
    def trader(self):
        return self._trader

    @property
    def credit(self):
        return self._credit

    @property
    def future(self):
        return self._future


class OtcHisDBHandler(TwseHisDBHandler):

    def __init__(self, **kwargs):
        super(OtcHisDBHandler, self).__init__(**copy.deepcopy(kwargs))
        self._debug = kwargs.pop('debug', False)
        db = 'otchisdb' if not self._debug else 'testotchisdb'
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect(db, host=host, port=port, alias=db)
        otchiscoll = switch(OtcHisColl, db)
        kwargs = {
            'stock': {
                'coll': otchiscoll,
                'debug': self._debug
            },
            'trader': {
                'coll': otchiscoll,
                'debug': self._debug
            },
            'credit': {
                'coll': otchiscoll,
                'debug': self._debug
            },
            'future': {
                'coll': otchiscoll,
                'debug': self._debug
            }
        }
        self._stock = OtcStockHisDBHandler(**kwargs['stock'])
        self._trader = OtcTraderHisDBHandler(**kwargs['trader'])
        self._credit = OtcCreditHisDBHandler(**kwargs['credit'])
        self._future = OtcFutureHisDBHandler(**kwargs['future'])


class TwseStockHisDBHandler(object):

    def __init__(self, **kwargs):
        self._coll = kwargs.pop('coll', None)
        self._debug = kwargs.pop('debug', False)
        kwargs = {
            'id': {
                'debug': self._debug,
                'opt': 'twse'
            }
        }
        self._id = TwseIdDBHandler(**kwargs['id'])
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

    def update_raw(self, item):
        self.insert_raw(item)

    def delete_raw(self, item):
        pass

    def insert_raw(self, item):
        """ bluk update stock part """
        keys = [k for k,v in StockData._fields.iteritems() if k not in ['id']]
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

    def query_raw(self, starttime, endtime, stockids=[], base='stock', order=['-totalvolume'], limit=10, callback=None):
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
        finalize_f = """
        """
        assert(set([o[1:] for o in order]) <= set(['totalvolume', 'totaldiff']))
        bufwin = (endtime - starttime).days
        cursor = self._coll.objects(Q(date__gte=starttime) & Q(date__lte=endtime) & Q(stockid__in=stockids))
        results = cursor.map_reduce(map_f, reduce_f, 'stockmap')
        results = list(results)
        reorder = lambda k: map(lambda x: k.value[x[1:]] if x.startswith('+') else -k.value[x[1:]], order)
        pool = sorted(results, key=reorder)[:limit]
        retval = []
        for it in pool:
            coll = { 'datalist': [] }
            for data in sorted(it.value['data'], key=lambda x: x['date']):
                coll['datalist'].append(data)
            coll.update({
                # key
                'date': endtime,
                'bufwin': bufwin,
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
        """ callback as pandas df """
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


class TwseTraderHisDBHandler(object):

    def __init__(self, **kwargs):
        self._coll = kwargs['coll']
        self._debug = kwargs['debug']
        kwargs = {
            'id': {
                'debug': self._debug,
                'opt': 'twse'
            }
        }
        self._id = TwseIdDBHandler(**kwargs['id'])
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

    def update_raw(self, item):
        self.insert_raw(item)

    def delete_raw(self, item):
        pass

    def insert_raw(self, item):
        """ bluk update trader part """
        keys = [k for k,v in TraderData._fields.iteritems() if k not in ['id']]
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

    def query_raw(self, starttime, endtime, stockids=[], traderids=[], base='stock', order=['-totalvolume'], limit=10, callback=None):
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
                                ratio = parseFloat(ratio.toFixed(2));
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
                            data: [{
                                date: this.date,
                                traderid: this.toplist[i].traderid,
                                tradernm: this.toplist[i].tradernm,
                                ratio: ratio,
                                avgbuyprice: avgbuyprice,
                                avgsellprice: avgsellprice,
                                buyvolume: buyvolume,
                                sellvolume: sellvolume
                            }]
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
        finalize_f = """
        """
        assert(set([o[1:] for o in order]) <= set(['totalvolume', 'totalbuyvolume', 'totalsellvolume']))
        bufwin = (endtime - starttime).days
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
        mkey = 'stockid' if base == 'stock' else 'traderid'
        mids = stockids if base == 'stock' else traderids
        results = [i for i in results if i.key[mkey] in mids]
        reorder = lambda k: map(lambda x: k.value[x[1:]] if x.startswith('x') else -k.value[x[1:]], order)
        pool = sorted(results, key=reorder)[:limit]
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
                'bufwin': bufwin,
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
        """ callback as pandas df """
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
        """ get alias map as virtual nick name to physical name """
        pool = list(filter(lambda x: x['alias'] in aliases, self._cache))
        for it in aliases:
            for i in pool:
                if i['alias'] == it:
                    yield i['stockid'] if base == 'stock' else i['traderid']


class TwseCreditHisDBHandler(object):

    def __init__(self, **kwargs):
        self._coll = kwargs.pop('coll', None)
        self._debug = kwargs.pop('debug', False)
        kwargs = {
            'id': {
                'debug': self._debug,
                'opt': 'twse'
            }
        }
        self._id = TwseIdDBHandler(**kwargs['id'])
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

    def update_raw(self, item):
        pass

    def delete_raw(self, item):
        pass

    def insert_raw(self, item):
        """ bluk update credit part """
        keys = [k for k,v in CreditData._fields.iteritems() if k not in ['id']]
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

    def query_raw(self, starttime, endtime, stockids=[], base='stock', order=['-financeused'], limit=10, callback=None):
        """ return orm
        <stockid>                                         | <stockid> ...
                    financeused| financetrend| bearishused| ...|
        20140928    100        | 101         |        999 | ...|
        20140929    100        | 102         |        999 | ...|
        """
        map_f = """
            function () {
                try {
                    var key =  { stockid : this.stockid };
                    var financetrend = 0;
                    var financeused = 0;
                    var bearishtrend = 0;
                    var bearishused = 0;
                    if (this.finance.preremain > 0) {
                        financetrend = (this.finance.curremain - this.finance.preremain) / this.finance.preremain;
                        financetrend = parseFloat(financetrend.toFixed(2));
                    }
                    if (this.finance.limit > 0) {
                        financeused = this.finance.curremain / this.finance.limit * 100;
                        financeused = parseFloat(financeused.toFixed(2));
                    }
                    if (this.bearish.preremain > 0) {
                        bearishtrend = (this.bearish.curremain - this.bearish.preremain) / this.bearish.preremain;
                        bearishtrend = parseFloat(bearishtrend.toFixed(2));
                    }
                    if (this.bearish.limit > 0) {
                        bearishused = this.bearish.curremain / this.bearish.limit * 100;
                        bearishused = parseFloat(bearishused.toFixed(2));
                    }
                    var value = {
                        financetrend: financetrend,
                        financeused: financeused,
                        bearishtrend: bearishtrend,
                        bearishused: bearishused,
                        data: [{
                            date: this.date,
                            financebuyvolume: this.finance.buyvolume,
                            financesellvolume: this.finance.sellvolume,
                            financeused: financeused,
                            bearishbuyvolume: this.bearish.buyvolume,
                            bearishsellvolume: this.bearish.sellvolume,
                            bearishused: bearishused
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
                    financetrend: 0,
                    financeused: 0,
                    bearishtrend: 0,
                    bearishtrend: 0,
                    data: []
                };
                if (values.length == 0) {
                    return redval;
                }
                for (var i=0; i < values.length; i++) {
                    redval.financetrend += values[i].financetrend;
                    redval.financeused += values[i].financeused;
                    redval.bearishtrend += values[i].bearishtrend;
                    redval.bearishused += values[i].bearishused;
                    redval.data = values[i].data.concat(redval.data);
                }
                return redval;
            }
        """
        finalize_f = """
        """
        assert(set([o[1:] for o in order]) <= set(['financeused', 'bearishused']))
        bufwin = (endtime - starttime).days
        cursor = self._coll.objects(Q(date__gte=starttime) & Q(date__lte=endtime) & Q(stockid__in=stockids))
        results = cursor.map_reduce(map_f, reduce_f, 'creditmap')
        results = list(results)
        reorder = lambda k: map(lambda x: k.value[x[1:]] if x.startswith('x') else -k.value[x[1:]], order)
        pool = sorted(results, key=reorder)[:limit]
        retval = []
        for it in pool:
            coll = { 'datalist': [] }
            for data in sorted(it.value['data'], key=lambda x: x['date']):
                coll['datalist'].append(data)
            coll.update({
                'date': endtime,
                'stockid': it.key['stockid'],
                'stocknm': self._id.stock.get_name(it.key['stockid']),
                'bufwin': bufwin,
                'order': order
            })
            retval.append(coll)
        return callback(retval) if callback else retval

    def to_pandas(self, cursor):
        """ callback to pandas df """
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


class TwseFutureHisDBHandler(object):

    def __init__(self, **kwargs):
        self._coll = kwargs.pop('coll', None)
        self._debug = kwargs.pop('debug', False)
        kwargs = {
            'id': {
                'debug': self._debug,
                'opt': 'twse'
            }
        }
        self._id = TwseIdDBHandler(**kwargs['id'])
        self._ids = []

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids


class OtcStockHisDBHandler(TwseStockHisDBHandler):

    def __init__(self, **kwargs):
        super(OtcStockHisDBHandler, self).__init__(**copy.deepcopy(kwargs))
        kwargs = {
            'id': {
                'debug': kwargs['debug'],
                'opt': 'otc'
            }
        }
        self._id = OtcIdDBHandler(**kwargs['id'])

class OtcTraderHisDBHandler(TwseTraderHisDBHandler):

    def __init__(self, **kwargs):
        super(OtcTraderHisDBHandler, self).__init__(**copy.deepcopy(kwargs))
        kwargs = {
            'id': {
                'debug': kwargs['debug'],
                'opt': 'otc'
            }
        }
        self._id = OtcIdDBHandler(**kwargs['id'])

class OtcCreditHisDBHandler(TwseCreditHisDBHandler):

    def __init__(self, **kwargs):
        super(OtcCreditHisDBHandler, self).__init__(**copy.deepcopy(kwargs))
        kwargs = {
            'id': {
                'debug': kwargs['debug'],
                'opt': 'otc'
            }
        }
        self._id = OtcIdDBHandler(**kwargs['id'])

class OtcFutureHisDBHandler(TwseFutureHisDBHandler):

    def __init__(self, **kwargs):
        super(OtcFutureHisDBHandler, self).__init__(**copy.deepcopy(kwargs))
        kwargs = {
            'id': {
                'debug': kwargs['debug'],
                'opt': 'otc'
            }
        }
        self._id = OtcIdDBHandler(**kwargs['id'])
