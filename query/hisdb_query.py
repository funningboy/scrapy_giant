
from datetime import datetime
from bson.code import Code
import traceback
import pandas as pd
import numpy as np
import pytz
from collections import OrderedDict
import json
from bson import json_util

from bin.mongodb_driver import *
from bin.logger import Logger

__all__ = ['TwseHisDBQuery', 'OtcHisDBQuery']

class BaseHisDBQuery(object):

    def __init__(self):
        self._client = connect_mongodb_service()
        self._db = self._client.twsedb
        self._coll = self._client.twsedb.twsehiscoll
        self._coll.ensure_index([('date', -1), ('stockid', 1), ('stocknm', 1)])
        self._stockmap = OrderedDict()
        self._tradermap = OrderedDict()

    @property
    def stockmap(self):
        return self._stockmap

    @property
    def tradermap(self):
        return self._tradermap

    def find_stockmap(self, stockid, nickname):
        if stockid in self._stockmap:
            if nickname in self._stockmap[stockid]:
                return self._stockmap[stockid][nickname]

    def find_tradermap(self, traderid, nickname):
        if traderid in self._tradermap:
            if nickname in self._tradermap[traderid]:
                return self._tradermap[traderid][nickname]

    def get_stock_data(self, starttime, endtime, stockids=[]):
        """ get stock data
        <stockid>                               | <stockid> ...
                    open| high| low|close|volume|          | open | ...
        20140928    100 | 101 | 99 | 100 | 100  | 20140928 | 11   | ...
        20140929    100 | 102 | 98 | 99  | 99   | 20140929 | 11   | ...
        """
        # query_exchange_from_db
        imap = Code(' \
            function () { \
                var key =  { stockid : this.stockid, date : this.date };\
                var value = { \
                    open : this.data.open, \
                    high : this.data.high, \
                    low : this.data.low, \
                    close : this.data.close, \
                    volume : this.data.volume, \
                    price : this.data.close \
                }; \
                emit(key, value); \
            };')
        ireduce = Code('\
            function (key, values) { \
                var redval = { \
                    open : 0, \
                    high : 0, \
                    low : 0, \
                    close : 0, \
                    volume : 0, \
                    price : 0 \
                }; \
                if (values.length == 0) { \
                    return redval; \
                } \
                redval.open = values[0].open; \
                redval.high = values[0].high; \
                redval.low = values[0].low; \
                redval.close = values[0].close; \
                redval.volume = values[0].volume; \
                redval.price = values[0].price; \
                return redval; \
            };')
        iquery = {
            '$and': [
                {'date': {'$gte': starttime, '$lte': endtime}},
                {'stockid': {'$in': stockids}}
            ]}
        try:
            pool = self._coll.map_reduce(
                imap,
                ireduce,
                'query_exchange_from_db',
                query=iquery)
        except:
            Logger.error("%s" % (traceback.format_exc()))
            raise
        data = OrderedDict()
        for stockid in stockids:
            if stockid not in self._stockmap:
              self._stockmap.update({stockid: {}})
            cursor = pool.find({'_id.stockid': stockid})
            value, index = [], []
            for it in cursor:
                value.append(it['value'])
                index.append(pytz.timezone('UTC').localize(it['_id']['date']))
            if value and index:
                data.update({stockid: pd.DataFrame(value, index=index).fillna(0)})
        return pd.Panel(data)

    def get_toptrader_data(self, starttime, endtime, stockids=[], traderids=[],
            opt='stock', dtyp='buy', limit=10):
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
        # query_toptrader_from_db
        imap = Code(' \
            function () { \
                for (var i=0; i < this.%(toplist)s.length; i++) { \
                    var key =  { traderid : this.%(toplist)s[i].traderid, stockid : this.stockid };\
                    var volume = this.%(toplist)s[i].data.buyvolume - this.%(toplist)s[i].data.sellvolume; \
                    var value = { \
                        volume : volume, \
                        data : [ { date : this.date, volume : volume } ] \
                    }; \
                    emit(key, value); \
                } \
                };' % {
                    'toplist': 'topbuylist' if dtyp == 'buy' else 'topselllist'
                    }
        )
        ireduce = Code('\
            function (key, values) { \
                var redval = { \
                    volume : 0, \
                    data : [] \
                }; \
                if (values.length == 0) { \
                    return redval; \
                } \
                for (var i=0; i < values.length; i++) { \
                    redval.volume += values[i].volume; \
                    redval.data = values[i].data.concat(redval.data); \
                } \
                return redval; \
        };')
        # $elemMatch doesn't work for map reduce ...
        iquery = {
            '$and': [
                {'date': {'$gte': starttime, '$lte': endtime}}
        ]}
        try:
            pool = self._coll.map_reduce(
                imap,
                ireduce,
                'query_toptrader_from_db',
                query=iquery)
        except:
            Logger.error("%s"  %(traceback.format_exc()))
            raise

        direct = -1 if dtyp == 'buy' else 1
        keynm = 'topbuy' if dtyp == 'buy' else 'topsell'

        if opt == 'stock':
            data = OrderedDict()
            for stockid in stockids:
                if stockid not in self._stockmap:
                    self._stockmap.update({stockid: {}})
                if traderids:
                    cursor = pool.find({
                        '$and': [
                            {'_id.stockid': stockid},
                            {'_id.traderid': {'$in': traderids}}
                        ]}).sort('value.volume', direct).limit(limit)
                else:
                    cursor = pool.find({
                        '$and': [
                            {'_id.stockid': stockid}
                            ]}).sort('value.volume', direct).limit(limit)

                frame = OrderedDict()
                for i, it in enumerate(cursor):
                    key = "%s%d" % (keynm, i)
                    # store stock to trader map info
                    self._stockmap[stockid].update({key: it['_id']['traderid']})
                    index, value = [], []
                    for ii in it['value']['data']:
                        index.append(pytz.timezone('UTC').localize(ii['date']))
                        value.append(ii['volume'])
                    if index and value:
                        frame.update({key: pd.Series(value, index=index)})
                if frame:
                    data.update({stockid: pd.DataFrame(frame).fillna(0)})
            return pd.Panel(data)
        else:
            data = OrderedDict()
            for traderid in traderids:
                if traderid not in self._tradermap:
                    self._tradermap.update({traderid: {}})
                if stockids:
                    cursor = pool.find({
                        '$and': [
                            {'_id.traderid': traderid},
                            {'_id.stockid': {'$in': stockids}}
                        ]}).sort('value.volume', direct).limit(limit)
                else:
                    cursor = pool.find({
                        '$and': [
                            {'_id.traderid': traderid}
                            ]}).sort('value.volume', direct).limit(limit)
                frame = OrderedDict()
                for i, it in enumerate(cursor):
                    key = "%s%d" % (keynm, i)
                    # store trader to stock map info
                    self._tradermap[traderid].update({key: it['_id']['stockid']})
                    index, value = [], []
                    for ii in it['value']['data']:
                        index.append(pytz.timezone('UTC').localize(ii['date']))
                        value.append(ii['volume'])
                    if index and value:
                        frame.update({key: pd.Series(value, index=index)})
                if frame:
                    data.update({traderid: pd.DataFrame(frame).fillna(0)})
            return pd.Panel(data)

    def get_all_data(self, starttime, endtime, stockids=[], traderids=[]):
        """ get stock data and extended toptrader data if addtrader = True
        <stockid>
        index(date) | o  | h  | l | c | v | topbuy0_<trdid> | ... | topsell0_<trdid> ...|
        ---------------------------------------------------------------------------
        20140827    | 10 | 11 | 9 | 9 | 100 | 10          | 0   | -10 |  0 |
        """
        stockdt = self.get_stock_data(starttime, endtime, stockids)
        topbuydt = self.get_toptrader_data(starttime, endtime, stockids, traderids, 'stock', 'buy')
        topselldt = self.get_toptrader_data(starttime, endtime, stockids, traderids, 'stock', 'sell')
        return pd.concat([stockdt, topbuydt, topselldt], axis=2).fillna(0)

    def delete_all_data(self, starttime, endtime, stockids=[], traderids=[]):
        raise NotImplementedError

    def set_stock_data(self, item):
        for it in item:
            # update content if exists
            bulk = self._coll.initialize_ordered_bulk_op()
            bulk.find({
                'stockid': it['stockid'],
                'date': it['date'],
            }).update({
                '$set': {
                    'data': {
                        'open': it['open'],
                        'high': it['high'],
                        'low': it['low'],
                        'close': it['close'],
                        'volume': it['volume']
                    }
                }
            })
            rst = bulk.execute()
            if sum([rst['nMatched'], rst['nInserted'], rst['nModified']]) == 0:
                # insert new content
                bulk = self._coll.initialize_ordered_bulk_op()
                bulk.insert({
                    'stockid': it['stockid'],
                    'date': it['date'],
                    'data': {
                        'open': it['open'],
                        'high': it['high'],
                        'low': it['low'],
                        'close': it['close'],
                        'volume': it['volume']
                    },
                    'topbuylist': [],
                    'topselllist': []
                })
                bulk.execute()

    def set_trader_data(self, item):
        bulk = self._coll.initialize_ordered_bulk_op()
        bulk.find({
            'stockid': item['stockid'],
            'date': item['date']
        }).update({
            '$set': {
                'topbuylist': item['topbuylist'],
                'topselllist': item['topselllist']}
        })
        rst = bulk.execute()

        if sum([rst['nMatched'], rst['nInserted'], rst['nModified']]) == 0:
            # insert new content
            bulk = self._coll.initialize_ordered_bulk_op()
            bulk.insert({
                'stockid': item['stockid'],
                'date': item['date'],
                'data': {},
                'topbuylist': item['topbuylist'],
                'topselllist': item['topselllist']
            })
            bulk.execute()


class TwseHisDBQuery(BaseHisDBQuery):

    def __init__(self):
        super(TwseHisDBQuery, self).__init__()
        self._client = connect_mongodb_service()
        self._db = self._client.twsedb
        self._coll = self._client.twsedb.twsehiscoll
        self._coll.ensure_index([('date', -1), ('stockid', 1), ('stocknm', 1)])


class OtcHisDBQuery(BaseHisDBQuery):

    def __init__(self):
        super(OtcHisDBQuery, self).__init__()
        self._client = connect_mongodb_service()
        self._db = self._client.otcdb
        self._coll = self._client.otcdb.otchiscoll
        self._coll.ensure_index([('date', -1), ('stockid', 1), ('stocknm', 1)])
