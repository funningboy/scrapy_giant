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
    """ ref tests.py
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
        """ bulk update stock part """
        keys = [k for k,v in StockData._fields.iteritems() if k not in ['id', '_cls']]
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

    def query_raw(self, starttime, endtime, stockids=[], base='stock', constraint=None, order=None, limit=10, callback=None):
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
                    // as constraint/sort key
                    var totalhldiff = Math.abs(this.data.high - this.data.low);
                    totalhldiff = parseFloat(totalhldiff.toFixed(2));
                    var totalocdiff = Math.abs(this.data.open - this.data.close);
                    totalocdiff = parseFloat(totalocdiff.toFixed(2));
                    var value = {
                        sopen: this.data.open,
                        sclose: this.data.close,
                        svolume: this.data.volume,
                        eopen: this.data.open,
                        eclose: this.data.close,
                        evolume: this.data.volume,
                        totalvolume: this.data.volume,
                        totalhldiff: totalhldiff,
                        totalocdiff: totalocdiff,
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
                    sopen: 0,
                    sclose: 0,
                    svolume: 0,
                    eopen: 0,
                    eclose: 0,
                    evolume: 0,
                    totalvolume: 0,
                    totalhldiff: 0,
                    totalocdiff: 0,
                    avgvolume: 0,
                    data: []
                };
                for (var i=0; i < values.length; i++) {
                    if (i==0) {
                        redval.sopen = values[i].data[0]['open'];
                        redval.sclose = values[i].data[0]['close'];
                        redval.svolume = values[i].data[0]['volume'];
                    }
                    if (i == values.length-1) {
                        redval.eopen = values[i].data[0]['open'];
                        redval.eclose = values[i].data[0]['close'];
                        redval.evolume = values[i].data[0]['volume'];
                    }
                    redval.totalvolume += values[i].totalvolume;
                    redval.totalhldiff += values[i].totalhldiff;
                    redval.totalocdiff += values[i].totalocdiff;
                    redval.data = values[i].data.concat(redval.data);
                }
                if (values.length) {
                    redval.avgvolume = redval.totalvolume / values.length;
                    redval.avgvolume = parseFloat(redval.avgvolume.toFixed(2));
                }
                return redval;
            }
        """
        finalize_f = """
        """
        bufwin = (endtime - starttime).days
        cursor = self._coll.objects(Q(date__gte=starttime) & Q(date__lte=endtime) & Q(stockid__in=stockids))
        results = list(cursor.map_reduce(map_f, reduce_f, 'stockmap'))
        if constraint:
            results = filter(constraint, results)
        if order:
            results = sorted(results, key=order)[:limit]
        retval = []
        for it in results:
            coll = { 'datalist': [] }
            for data in sorted(it.value['data'], key=lambda x: x['date']):
                coll['datalist'].append(data)
            coll.update({
                # key
                'date': endtime,
                'bufwin': bufwin,
                'stockid': it.key['stockid'],
                'stocknm': self._id.stock.get_name(it.key['stockid']),
                # value
                'totalvolume': it.value['totalvolume'],
                'totalhldiff': it.value['totalhldiff'],
                'totalocdiff': it.value['totalocdiff']
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
        """ bulk update trader part """
        keys = [k for k,v in TraderData._fields.iteritems() if k not in ['id', '_cls']]
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

    def query_raw(self, starttime, endtime, stockids=[], traderids=[], base='stock', constraint=None, order=None, limit=10, callback=None):
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
                        var keepbuy = 0;
                        var keepsell = 0;
                        var buyratio = 0;
                        var sellratio = 0;
                        var maxvolume = Math.max(buyvolume, sellvolume);
                        maxvolume = parseFloat(maxvolume.toFixed(2));
                        var minvolume = Math.min(buyvolume, sellvolume);
                        minvolume = parseFloat(minvolume.toFixed(2));
                        var maxprice = Math.max(avgbuyprice, avgsellprice);
                        maxprice = parseFloat(maxprice.toFixed(2));
                        var minprice = Math.min(avgbuyprice, avgsellprice);
                        minprice = parseFloat(minprice.toFixed(2));
                        if (this.data.volume >0) {
                            if (buyvolume >0) {
                                buyratio = buyvolume / this.data.volume * 100;
                                buyratio = parseFloat(buyratio.toFixed(2));
                                keepbuy = 1;
                            }
                            if (sellvolume >0) {
                                sellratio = sellvolume / this.data.volume * 100;
                                sellratio = parseFloat(sellratio.toFixed(2));
                                keepsell = 1;
                            }
                        }
                        // as constraint/sort key
                        var value = {
                            totalvolume: totalvolume,
                            totalbuyvolume: buyvolume,
                            totalsellvolume: sellvolume,
                            totalkeepbuy: keepbuy,
                            totalkeepsell: keepsell,
                            totalbuyratio: buyratio,
                            totalsellratio: sellratio,
                            ebuyratio: buyratio,
                            esellratio: sellratio,
                            data: [{
                                date: this.date,
                                traderid: this.toplist[i].traderid,
                                tradernm: this.toplist[i].tradernm,
                                keepbuy: keepbuy,
                                keepsell: keepsell,
                                buyratio: buyratio,
                                sellratio: sellratio,
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
                    totalkeepbuy: 0,
                    totalkeepsell: 0,
                    totalbuyratio: 0,
                    totalsellratio: 0,
                    ebuyratio: 0,
                    esellratio: 0,
                    data: []
                };
                for (var i=0; i < values.length; i++) {
                    if (i == values.length-1) {
                        redval.ebuyratio = values[i].data[0]['buyratio'];
                        redval.esellratio = values[i].data[0]['sellratio'];
                    }
                    redval.totalvolume += values[i].totalvolume;
                    redval.totalbuyvolume += values[i].totalbuyvolume;
                    redval.totalsellvolume += values[i].totalsellvolume;
                    redval.totalkeepbuy += values[i].totalkeepbuy;
                    redval.totalkeepsell += values[i].totalkeepsell;
                    redval.totalbuyratio += values[i].totalbuyratio;
                    redval.totalsellratio += values[i].totalsellratio;
                    redval.data = values[i].data.concat(redval.data);
                }
                return redval;
            }
        """
        finalize_f = """
        """
        bufwin = (endtime - starttime).days
        if stockids and traderids:
            cursor = self._coll.objects(
                Q(date__gte=starttime) & Q(date__lte=endtime) &
                (Q(stockid__in=stockids) & Q(toplist__traderid__in=traderids)))
        else:
            cursor = self._coll.objects(
                Q(date__gte=starttime) & Q(date__lte=endtime) &
                (Q(stockid__in=stockids) | Q(toplist__traderid__in=traderids)))
        results = list(cursor.map_reduce(map_f, reduce_f, 'toptradermap'))
        retval = []
        sort = [('stockid', stockids), ('traderid', traderids)] if base == 'stock' else [('traderid', traderids), ('stockid', stockids)]
        if constraint:
            results = filter(constraint, results)
        for k, s in sort:
            if s:
                results = list(filter(lambda x: x.key[k] in s, results))
        if order:
            results = sorted(results, key=order)[:limit]
        for i, it in enumerate(results):
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
                'tradernm': self._id.trader.get_name(it.key['traderid']),
                'stocknm': self._id.stock.get_name(it.key['stockid']),
                # value
                'totalvolume': it.value['totalvolume'],
                'totalbuyvolume': it.value['totalbuyvolume'],
                'totalsellvolume': it.value['totalsellvolume'],
                'totalkeepbuy': it.value['totalkeepbuy'],
                'totalkeepsell': it.value['totalkeepsell'],
                'totalbuyratio': it.value['totalbuyratio'],
                'totalsellratio': it.value['totalsellratio'],
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
                            "%s_buyratio" % (it['alias']): i['buyratio'],
                            "%s_sellratio" % (it['alias']): i['sellratio'],
                            "%s_keepbuy" % (it['alias']): i['keepbuy'],
                            "%s_keepsell" % (it['alias']): i['keepsell'],
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
        """ bulk update credit part """
        keys = [k for k,v in CreditData._fields.iteritems() if k not in ['id', '_cls']]
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

    def query_raw(self, starttime, endtime, stockids=[], base='stock', constraint=None, order=None, limit=10, callback=None):
        """ return orm
        <stockid>                                         | <stockid> ...
                    financeremain| financetrend| bearishremain| ...|
        20140928    100        | 101         |        999 | ...|
        20140929    100        | 102         |        999 | ...|
        """
        map_f = """
            function () {
                try {
                    var key =  { stockid : this.stockid };
                    var financetrend = 0;
                    var financeremain = 0;
                    var bearishtrend = 0;
                    var bearishremain = 0;
                    var bearfinaratio = 0;
                    if (this.finance.preremain > 0) {
                        financetrend = (this.finance.curremain - this.finance.preremain) / this.finance.preremain;
                        financetrend = parseFloat(financetrend.toFixed(2));
                    }
                    if (this.finance.limit > 0) {
                        financeremain = this.finance.curremain / this.finance.limit * 100;
                        financeremain = parseFloat(financeremain.toFixed(2));
                    }
                    if (this.bearish.preremain > 0) {
                        bearishtrend = (this.bearish.curremain - this.bearish.preremain) / this.bearish.preremain;
                        bearishtrend = parseFloat(bearishtrend.toFixed(2));
                    }
                    if (this.bearish.limit > 0) {
                        bearishremain = this.bearish.curremain / this.bearish.limit * 100;
                        bearishremain = parseFloat(bearishremain.toFixed(2));
                    }
                    if (this.finance.curremain) {
                        bearfinaratio = this.bearish.curremain / this.finance.curremain * 100;
                        bearfinaratio = parseFloat(bearfinaratio.toFixed(2));
                    }
                    // as constraint/sort key
                    var value = {
                        totalfinanceremain: financeremain,
                        totalbearishremain: bearishremain,
                        efinanceremain: financeremain,
                        efinancetrend: financetrend,
                        ebearishremain: bearishremain,
                        ebearishtrend: bearishtrend,
                        ebearfinaratio: bearfinaratio,
                        data: [{
                            date: this.date,
                            financebuyvolume: this.finance.buyvolume,
                            financesellvolume: this.finance.sellvolume,
                            financeremain: financeremain,
                            financetrend: financetrend,
                            bearishbuyvolume: this.bearish.buyvolume,
                            bearishsellvolume: this.bearish.sellvolume,
                            bearishremain: bearishremain,
                            bearishtrend: bearishtrend,
                            bearfinaratio: bearfinaratio
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
                    totalfinanceremain: 0,
                    totalbearishremain: 0,
                    efinanceremain: 0,
                    efinancetrend: 0,
                    ebearishremain: 0,
                    ebearishtrend: 0,
                    ebearfinaratio: 0,
                    data: []
                };
                for (var i=0; i < values.length; i++) {
                    if (i == values.length-1) {
                        redval.efinancetrend = values[i].data[0]['financetrend'];
                        redval.efinanceremain = values[i].data[0]['financeremain'];
                        redval.ebearishtrend = values[i].data[0]['bearishtrend'];
                        redval.ebearishremain = values[i].data[0]['bearishremain'];
                        redval.ebearfinaratio = values[i].data[0]['bearfinaratio'];
                    }
                    redval.totalfinanceremain += values[i].totalfinanceremain;
                    redval.totalbearishremain += values[i].totalbearishremain;
                    redval.data = values[i].data.concat(redval.data);
                }
                return redval;
            }
        """
        finalize_f = """
        """
        bufwin = (endtime - starttime).days
        cursor = self._coll.objects(Q(date__gte=starttime) & Q(date__lte=endtime) & Q(stockid__in=stockids))
        results = list(cursor.map_reduce(map_f, reduce_f, 'creditmap'))
        if constraint:
            results = filter(constraint, results)
        if order:
            results = sorted(results, key=order)[:limit]
        retval = []
        for it in results:
            coll = { 'datalist': [] }
            for data in sorted(it.value['data'], key=lambda x: x['date']):
                coll['datalist'].append(data)
            coll.update({
                #key
                'date': endtime,
                'stockid': it.key['stockid'],
                'stocknm': self._id.stock.get_name(it.key['stockid']),
                'bufwin': bufwin,
                # value
                'totalfinanceremain': it.value['totalfinanceremain'],
                'totalbearishremain': it.value['totalbearishremain']
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

    @property
    def coll(self):
        return self._coll

    def update_raw(self, item):
        pass

    def delete_raw(self, item):
        pass

    def insert_raw(self, item):
        """ bulk update credit part """
        keys = [k for k,v in FutureData._fields.iteritems() if k not in ['id', '_cls']]
        for it in item:
            data = {k:v for k, v in it.items() if k in keys}
            data = FutureData(**data)
            cursor = self._coll.objects(Q(date=it['date']) & Q(stockid=it['stockid']))
            cursor = list(cursor)
            coll = self._coll() if len(cursor) == 0 else cursor[0]
            coll.stockid = it['stockid']
            coll.date = it['date']
            coll.future = data
            coll.save()

    def query_raw(self, starttime, endtime, stockids=[], base='stock', constraint=None, order=None, limit=10, callback=None):
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
                    var diff = this.future.high - this.future.low;
                    var edfodiff = this.data.open - this.future.open;
                    edfodiff = parseFloat(edfodiff.toFixed(2));
                    var edfhdiff = this.data.high - this.future.high;
                    edfhdiff = parseFloat(edfhdiff.toFixed(2));
                    var edfldiff = this.data.low - this.future.low;
                    edfldiff = parseFloat(edfldiff.toFixed(2));
                    var edfcdiff = this.data.close - this.future.close;
                    edfcdiff = parseFloat(edfcdiff.toFixed(2));
                    var totalhldiff = Math.abs(this.future.high - this.future.low);
                    totalhldiff = parseFloat(totalhldiff.toFixed(2));
                    var totalocdiff = Math.abs(this.future.open - this.future.close);
                    totalocdiff = parseFloat(totalocdiff.toFixed(2));
                    // as constraint/sort key
                    var value = {
                        totalvolume: this.future.volume,
                        totalhldiff: totalhldiff,
                        totalocdiff: totalocdiff,
                        edfodiff: edfodiff,
                        edfhdiff: edfhdiff,
                        edfldiff: edfldiff,
                        edfcdiff: edfcdiff, 
                        data: [{
                            date: this.date,
                            fopen: this.future.open,
                            fhigh: this.future.high,
                            flow: this.future.low,
                            fclose: this.future.close,
                            fprice: this.future.close,
                            fvolume: this.future.volume,
                            fsetprice: this.future.setprice,
                            funtrdcount: this.future.untrdcount,
                            fbestbuy: this.future.bestbuy,
                            fbestsell: this.future.bestsell,
                            dfodiff: edfodiff,
                            dfhdiff: edfhdiff,
                            dfldiff: edfldiff,
                            dfcdiff: edfcdiff
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
                    totalhldiff: 0,
                    totalocdiff: 0,
                    edfodiff: 0,
                    edfhdiff: 0,
                    edfldiff: 0,
                    edfcdiff: 0,
                    data: []
                };
                for (var i=0; i < values.length; i++) {
                    if (i == values.length-1) {
                        redval.edfodiff = values[i].data[0]['dfodiff'];
                        redval.edfhdiff = values[i].data[0]['dfhdiff'];
                        redval.edfldiff = values[i].data[0]['dfldiff'];
                        redval.edfcdiff = values[i].data[0]['dfcdiff'];
                    }
                    redval.totalvolume += values[i].totalvolume;
                    redval.totalhldiff += values[i].totalhldiff;
                    redval.totalocdiff += values[i].totalocdiff;
                    redval.data = values[i].data.concat(redval.data);
                }
                return redval;
            }
        """
        finalize_f = """
        """
        bufwin = (endtime - starttime).days
        cursor = self._coll.objects(Q(date__gte=starttime) & Q(date__lte=endtime) & Q(stockid__in=stockids))
        results = list(cursor.map_reduce(map_f, reduce_f, 'futuremap'))
        if constraint:
            results = filter(constraint, results)
        if order:
            results = sorted(results, key=order)[:limit]
        retval = []
        for it in results:
            coll = { 'datalist': [] }
            for data in sorted(it.value['data'], key=lambda x: x['date']):
                coll['datalist'].append(data)
            coll.update({
                # key
                'date': endtime,
                'bufwin': bufwin,
                'stockid': it.key['stockid'],
                'stocknm': self._id.stock.get_name(it.key['stockid']),
                # value
                'totalvolume': it.value['totalvolume'],
                'totalhldiff': it.value['totalhldiff'],
                'totalocdiff': it.value['totalocdiff'],
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
