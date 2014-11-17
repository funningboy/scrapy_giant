# -*- coding: utf-8 -*-

import pandas as pd
import pytz
import json
from collections import OrderedDict, defaultdict
from bson import json_util

from mongoengine import *
from mongoengine.connection import get_connection, get_db
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.models import (
    TwseHisColl, OtcHisColl, StockData, TraderData,
    TraderInfo, TraderMapColl, TraderMapData
)

# use mongoengine(high level mongodb drive) as ORM data backend for Django access

__all__ = ['TwseHisDBHandler', 'OtcHisDBHandler']


class TwseHisDBHandler(object):

    def __init__(self):
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('twsehisdb', host=host, port=port, alias='twsehisdb')
        twsehiscoll = switch(TwseHisColl, 'twsehisdb')
        self._stock = StockHisDBHandler(twsehiscoll)
        self._trader = TraderHisDBHandler(twsehiscoll)

    @property
    def stock(self):
        return self._stock

    @property
    def trader(self):
        return self._trader


class OtcHisDBHandler(TwseHisDBHandler):

    def __init__(self):
        super(OtcHisDBHandler, self).__init__()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('otchisdb', host=host, port=port, alias='otchisdb')
        otchiscoll = switch(OtcHisColl, 'otchisdb')
        self._stock = StockHisDBHandler(otchiscoll)
        self._trader = TraderHisDBHandler(otchiscoll)


class StockHisDBHandler(object):

    def __init__(self, coll):
        """ specified hiscoll as twse/otc """
        self._coll = coll
        self._ids = []

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids

    def insert(self, item):
        """ insert stock item to db """
        for it in item:
            data = {
                'open': it ['open'],
                'high': it['high'],
                'low': it['low'],
                'close': it['close'],
                'volume': it['volume']
            }
            data = StockData(**data)
            cursor = self._coll.objects(Q(date=it['date']) & Q(stockid=it['stockid']))
            if cursor.count() == 0:
                coll = self._coll().save()
            else:
                coll = list(cursor)[0]
            coll.stockid = it['stockid']
            coll.date = it['date']
            coll.data = data
            coll.save()

    def query(self, starttime, endtime, stockids=[]):
        """ return orm
        <stockid>                               | <stockid> ...
                    open| high| low|close|volume|          | open | ...
        20140928    100 | 101 | 99 | 100 | 100  | 20140928 | 11   | ...
        20140929    100 | 102 | 98 | 99  | 99   | 20140929 | 11   | ...
        """
        cursor = self._coll.objects(Q(date__gte=starttime) & Q(date__lte=endtime) & Q(stockid__in=stockids))
#        return cursor.values_list('date', 'stockid', 'data')
        return cursor

    def to_pandas(self, cursor):
        """ transform orm to pandas panel
        """
        stockids = set([x.stockid for x in cursor])
        item = OrderedDict()
        for stockid in stockids:
            pool = list(filter(lambda x: x.stockid==stockid, cursor))
            index, data = [], []
            for it in pool:
                index.append(pytz.timezone('UTC').localize(it.date))
                data.append(it.data)
            if index and data:
                item.update({
                    stockid: pd.DataFrame(data, index=index).fillna(0)
                 })
        return pd.Panel(item)


    def to_json(self, cursor):
        """ transform orm to json stream
        """
        return cursor.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)


class TraderHisDBHandler(object):

    def __init__(self, coll):
        """ specified hiscoll as twse/otc """
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('traderhisdb', host=host, port=port, alias='traderhisdb')
        self._mapcoll = switch(TraderMapColl, 'traderhisdb')
        self._mapcoll.drop_collection()
        self._coll = coll
        self._ids = []

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids

    def insert(self, item):
        """ insert trader item to db """
        topbuylist, topselllist = [], []
        for it in item['topbuylist']:
            data = {
                'avgbuyprice': it['data']['avgbuyprice'],
                'buyvolume': it['data']['buyvolume'],
                'avgsellprice': it['data']['avgsellprice'],
                'sellvolume': it['data']['sellvolume']
            }
            topbuylist.append(
                TraderInfo(
                    traderid=it['traderid'],
                    tradernm=it['tradernm'],
                    data=TraderData(**data))
            )
        for it in item['topselllist']:
            data = {
                'avgbuyprice': it['data']['avgbuyprice'],
                'buyvolume': it['data']['buyvolume'],
                'avgsellprice': it['data']['avgsellprice'],
                'sellvolume': it['data']['sellvolume']
            }
            topselllist.append(
                TraderInfo(
                    traderid=it['traderid'],
                    tradernm=it['tradernm'],
                    data=TraderData(**data))
            )
        cursor = self._coll.objects(Q(date=item['date']) & Q(stockid=item['stockid']))
        if cursor.count() == 0:
            coll = self._coll().save()
        else:
            coll = list(cursor)[0]
        coll.stockid = item['stockid']
        coll.date = item['date']
        coll.topbuylist = topbuylist
        coll.topselllist = topselllist
        coll.save()

    def query(self, starttime, endtime, stockids=[], traderids=[],
            base='stock', opt='buy', limit=10):
        """ get rank topbuy/topsell volume stock/trader data
            <stockid>                                               <stockid>
                     | topbuy0_<traderid> | topbuy1 | ... topbuy10 |          | topbuy0_<traderid>
            20140928 |  100               |   30    |              | 20140928 | ...
            20140929 |    0               |   20    |              | 20140929 | ...
            -------------------------------------------------------------------------
                        100                   50

            <traderid>                                              <traderid>
                     | topbuy0_<stockid> | topbuy1  | ... topbuy10 |          | topbuy0_<traderid>
            20140928 |  100               |   30    |              | 20140928 | ...
            20140929 |    0               |   20    |              | 20140929 | ...
            -------------------------------------------------------------------------
                        100                   50
        """
        map_f = """
            function () {
                for (var i=0; i < this.%(toplist)s.length; i++) {
                    var key =  { traderid : this.%(toplist)s[i].traderid, stockid : this.stockid };
                    var volume = Math.abs(this.%(toplist)s[i].data.buyvolume - this.%(toplist)s[i].data.sellvolume);
                    var value = {
                        volume : volume,
                        data : [ { date : this.date, volume : volume } ]
                    };
                    emit(key, value);
                }
            }
        """ % { 'toplist': 'topbuylist' if opt == 'buy' else 'topselllist' }
        reduce_f = """
            function (key, values) {
                var redval = {
                    volume : 0,
                    data : []
                };
                if (values.length == 0) {
                    return redval;
                }
                for (var i=0; i < values.length; i++) {
                    redval.volume += values[i].volume;
                    redval.data = values[i].data.concat(redval.data);
                }
                return redval;
            }
        """
        cursor = self._coll.objects(
            Q(date__gte=starttime) & Q(date__lte=endtime) &
            (Q(stockid__in=stockids) | Q(topbuylist__traderid__in=traderids) | Q(topselllist__traderid__in=traderids)))
        results = cursor.map_reduce(
            map_f,
            reduce_f,
            'toptradermap',
            )
        ids = stockids if base == 'stock' else traderids
        mkey = 'stockid' if base == 'stock' else 'traderid'
        vkey = 'traderid' if base == 'stock' else 'stockid'
        for id in ids:
            pool = list(filter(lambda x: x.key[mkey]==id, results))
            pool = sorted(pool, lambda x: x.value['volume'], reverse=True)
            pool = pool[:limit]
            for i, it in enumerate(pool):
                coll = self._mapcoll().save()
                for data in it.value['data']:
                    coll.datalist.append(
                        TraderMapData(volume=data['volume'], date=data['date']))
                coll.traderid = it.key['traderid']
                coll.stockid = it.key['stockid']
                coll.alias = "topbuy%d" % (i) if opt == 'buy' else "topsell%d" % (i)
                coll.base = base
                coll.save()
        return self._mapcoll.objects()

    def to_pandas(self, cursor):
        """ transform orm to pandas panel
        """
        bases = list(set([it.base for it in cursor]))
        assert(len(bases)<2)
        item = OrderedDict()
        for it in cursor:
            index, data = [], []
            for ii in it.datalist:
                index.append(pytz.timezone('UTC').localize(ii.date))
                data.append({it.alias: ii.volume})
            if index and data:
                id = it.stockid if bases[0] == 'stock' else it.traderid
                item.update({
                    id: pd.DataFrame(data, index=index).fillna(0)
                 })
        return pd.Panel(item)

    def to_json(self, cursor):
        """ transform orm to json
        """
        return cursor.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)

    def map_alias(self, ids=[], base='stock', aliases=['topbuy0']):
        if base == 'stock':
            cursor = self._mapcoll.objects(Q(base=base) & Q(stockid__in=ids) & Q(alias__in=aliases))
            return [it.traderid for it in cursor]
        else:
            cursor = self._mapcoll.objects(Q(base=base) & Q(traderid__in=ids) & Q(alias__in=aliases))
            return [it.stockid for it in cursor]


