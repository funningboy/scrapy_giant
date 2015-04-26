# -*- coding: utf-8 -*-

import pandas as pd
import pytz
from collections import OrderedDict
from bson import json_util

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.models import *
# use mongoengine(high level mongodb drive) as ORM data backend for Django access

__all__ = ['TwseHisDBHandler', 'OtcHisDBHandler']


class TwseHisDBHandler(object):

    def __init__(self):
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('twsehisdb', host=host, port=port, alias='twsehisdb')
        twsehiscoll = switch(TwseHisColl, 'twsehisdb')
        self._stock = TwseStockHisDBHandler(twsehiscoll)
        self._trader = TwseTraderHisDBHandler(twsehiscoll)
        self._credit = TwseCreditDBHandler(twsehiscoll)

    @property
    def stock(self):
        return self._stock

    @property
    def trader(self):
        return self._trader

    @property
    def credit(self):
        return self._credit

    def transform_all_data(self, starttime, endtime, stockids=[], traderids=[], order='totalvolume', limit=10):
        """ transfrom stock/trader data as pandas panel """
        args = (starttime, endtime, stockids, order, limit, self._stock.to_pandas)
        stockdt = self._stock.query(*args)
        args = (starttime, endtime, list(stockdt.keys()), traderids, 'stock', order, limit, self._trader.to_pandas)
        traderdt = self._trader.query(*args)
        return pd.concat([stockdt, traderdt], axis=2).fillna(0)


class OtcHisDBHandler(TwseHisDBHandler):

    def __init__(self):
        super(OtcHisDBHandler, self).__init__()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('otchisdb', host=host, port=port, alias='otchisdb')
        otchiscoll = switch(OtcHisColl, 'otchisdb')
        self._stock = OtcStockHisDBHandler(otchiscoll)
        self._trader = OtcTraderHisDBHandler(otchiscoll)
        self._credit = OtcCreditHisDBHandler(otchiscoll)


class TwseStockHisDBHandler(object):

    def __init__(self, coll):
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('stockmapdb', host=host, port=port, alias='stockmapdb')
        self._iddbhandler = TwseIdDBHandler()
        self._mapcoll = switch(StockMapColl, 'stockmapdb')
        self._mapcoll.drop_collection()
        self._coll = coll
        self._ids = []

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids

    def drop(self):
        self._mapcoll.drop_collection()
        self._ids = []

    def delete(self, item):
        pass

    def insert(self, item):
        keys = [k for k,v in StockData._fields.iteritems()]
        for it in item:
            dt = {k:v for k, v in it.items() if k in keys}
            data = StockData(**dt)
            cursor = self._coll.objects(Q(date=it['date']) & Q(stockid=it['stockid']))
            cursor = list(cursor)
            coll = self._coll() if len(cursor) == 0 else cursor[0]
            coll.stockid = it['stockid']
            coll.date = it['date']
            coll.data = data
            coll.save()

    def query(self, starttime, endtime, stockids=[], order='totalvolume', limit=10, callback=None):
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
        assert(order in ['totalvolume', 'totaldiff'])
        cursor = self._coll.objects(Q(date__gte=starttime) & Q(date__lte=endtime) & Q(stockid__in=stockids))
        results = cursor.map_reduce(map_f, reduce_f, 'stockmap')
        results = list(results)
        keys = [k for k,v in StockMapData._fields.iteritems()]
        pool = sorted(results, key=lambda x: x.value[order], reverse=True)[:limit]
        for it in pool:
            coll = self._mapcoll()
            for data in sorted(it.value['data'], key=lambda x: x['date']):
                dt = {k:v for k, v in data.items() if k in keys}
                coll.datalist.append(StockMapData(**dt))
            coll.stockid = it.key['stockid']
            coll.stocknm = self._iddbhandler.stock.get_name(it.key['stockid'])
            coll.url = ''
            coll.save()
        results = self._mapcoll.objects.all()
        return callback(results) if callback else results

    def to_pandas(self, cursor):
        item = OrderedDict()
        keys = [k for k,v in StockMapData._fields.iteritems()]
        for it in cursor:
            index, data = [], []
            for i in it.datalist:
                index.append(pytz.timezone('UTC').localize(i.date))
                dt = {k: getattr(i, k) for k in keys}
                data.append(dt)
            if index and data:
                id = it.stockid
                item.update({id: pd.DataFrame(data, index=index).fillna(0)})
        return pd.Panel(item)


class TwseTraderHisDBHandler(object):

    def __init__(self, coll):
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('tradermapdb', host=host, port=port, alias='tradermapdb')
        self._iddbhandler = TwseIdDBHandler()
        self._mapcoll = switch(TraderMapColl, 'tradermapdb')
        self._mapcoll.drop_collection()
        self._coll = coll
        self._ids = []

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids

    def drop(self):
        self._mapcoll.drop_collection()
        self._ids = []

    def delete(self, item):
        pass

    def insert(self, item):
        keys = [k for k,v in TraderData._fields.iteritems()]
        toplist = []
        for it in item['toplist']:
            dt = {k:v for k, v in it['data'].items() if k in keys}
            td = {
                'traderid': it['traderid'],
                'tradernm': it['tradernm'],
                'data': TraderData(**dt)
            }
            toplist.append(TraderInfo(**td))
        cursor = self._coll.objects(Q(date=item['date']) & Q(stockid=item['stockid']))
        cursor = list(cursor)
        coll = self._coll() if len(cursor) == 0 else cursor[0]
        coll.stockid = item['stockid']
        coll.date = item['date']
        coll.toplist = toplist
        coll.save()

    def query(self, starttime, endtime, stockids=[], traderids=[],
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
        assert(order in ['totalvolume', 'totalhit', 'totalbuyvolume', 'totalsellvolume', 'totaltradeprice', 'totaltradevolume'])
        keys = [k for k,v in TraderMapData._fields.iteritems()]
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
        for id in ids:
            pool = list(filter(lambda x: x.key[mkey]==id, results))
            pool = sorted(pool, key=lambda x: x.value['totalhit'], reverse=True)[:limit]
            for i, it in enumerate(pool):
                coll = self._mapcoll()
                for data in sorted(it.value['data'], key=lambda x: x['date']):
                    dt = {k:v for k, v in data.items() if k in keys}
                    coll.datalist.append(TraderMapData(**dt))
                coll.traderid = it.key['traderid']
                coll.stockid = it.key['stockid']
                coll.tradernm = self._iddbhandler.trader.get_name(it.key['traderid'])
                coll.stocknm = self._iddbhandler.stock.get_name(it.key['stockid'])
                coll.totalvolume = it.value['totalvolume']
                coll.totalbuyvolume = it.value['totalbuyvolume']
                coll.totalsellvolume = it.value['totalsellvolume']
                coll.totalhit = it.value['totalhit']
                coll.totaltradeprice = it.value['totaltradeprice']
                coll.totaltradevolume = it.value['totaltradevolume']
                coll.alias = "top%d" % (i)
                coll.save()
        results = self._mapcoll.objects.all()
        return callback(results) if callback else results

    def to_pandas(self, cursor, base='stock'):
        item = OrderedDict()
        ids = [it.stockid if base =='stock' else it.traderid for it in cursor]
        for id in ids:
            df = pd.DataFrame()
            pool = list(filter(lambda x: x.stockid==id, cursor)) if base == 'stock' else list(filter(lambda x: x.traderid==id, cursor))
            for it in pool:
                index, data= [], []
                for i in it.datalist:
                    index.append(pytz.timezone('UTC').localize(i.date))
                    dt = {
                        "%s_ratio" % (it.alias): i.ratio,
                        "%s_price" % (it.alias): i.price,
                        "%s_buyvolume" % (it.alias): i.buyvolume,
                        "%s_sellvolume" % (it.alias): i.sellvolume
                    }
                    data.append(dt)
                if index and data:
                    df = pd.concat([df, pd.DataFrame(data, index=index).fillna(0)], axis=1)
            item.update({id: df})
        return pd.Panel(item)

    def map_alias(self, ids=[], base='stock', aliases=['top0']):
        """ get alias map as virtual to physical map """
        if base == 'stock':
            cursor = self._mapcoll.objects(Q(stockid__in=ids) & Q(alias__in=aliases))
            cursor = list(cursor)
            return [it.traderid for it in cursor]
        else:
            cursor = self._mapcoll.objects(Q(traderid__in=ids) & Q(alias__in=aliases))
            cursor = list(cursor)
            return [it.stockid for it in cursor]


class TwseCreditDBHandler(object):

    def __init__(self, coll):
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('creditmapdb', host=host, port=port, alias='creditmapdb')
        self._iddbhandler = TwseIdDBHandler()
        self._mapcoll = switch(CreditMapColl, 'creditmapdb')
        self._mapcoll.drop_collection()
        self._coll = coll
        self._ids = []

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids

    def drop(self):
        self._mapcoll.drop_collection()
        self._ids = []

    def delete(self, item):
        pass

    def insert(self, item):
        keys = [k for k,v in CreditData._fields.iteritems()]
        for it in item:
            dt = {k:v for k, v in it.items() if k in keys}
            data = CreditData(**dt)
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

    def query(self, starttime, endtime, stockids=[], order='totalvolume', limit=10, callback=None):
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
        assert(order in ['financeinc', 'financedec', 'bearishinc', 'bearishdec'])
        cursor = self._coll.objects(Q(date__gte=starttime) & Q(date__lte=endtime) & Q(stockid__in=stockids))
        results = cursor.map_reduce(map_f, reduce_f, 'creditmap')
        results = list(results)
        keys = [k for k,v in CreditMapData._fields.iteritems()]
        pool = sorted(results, key=lambda x: x.value[order], reverse=True if order in ['financeinc', 'bearishinc'] else False)[:limit]
        for it in pool:
            coll = self._mapcoll()
            for data in sorted(it.value['data'], key=lambda x: x['date']):
                dt = {k:v for k, v in data.items() if k in keys}
                coll.datalist.append(CreditMapData(**dt))
            coll.stockid = it.key['stockid']
            coll.save()
        results = self._mapcoll.objects.all()
        return callback(results) if callback else results

    def to_pandas(self, cursor):
        item = OrderedDict()
        keys = [k for k,v in CreditMapData._fields.iteritems()]
        for it in cursor:
            index, data = [], []
            for i in it.datalist:
                index.append(pytz.timezone('UTC').localize(i.date))
                dt = {k: getattr(i, k) for k in keys}
                data.append(dt)
            if index and data:
                id = it.stockid
                item.update({id: pd.DataFrame(data, index=index).fillna(0)})
        return pd.Panel(item)


class OtcStockHisDBHandler(TwseStockHisDBHandler):
    def __init__(self, coll):
        super(OtcStockHisDBHandler, self).__init__(coll)
        self._iddbhandler = OtcIdDBHandler()

class OtcTraderHisDBHandler(TwseTraderHisDBHandler):
    def __init__(self, coll):
        super(OtcTraderHisDBHandler, self).__init__(coll)
        self._iddbhandler = OtcIdDBHandler()

class OtcCreditHisDBHandler(TwseCreditDBHandler):
    def __init__(self, coll):
        super(OtcCreditHisDBHandler, self).__init__(coll)
        self._iddbhandler = OtcIdDBHandler()
