
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import copy

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.models import TwseIdColl, OtcIdColl, TraderIdColl

__all__ = ['TwseIdDBHandler', 'OtcIdDBHandler', 'TraderIdDBHandler']


class TwseIdDBHandler(object):

    def __init__(self, **kwargs):
        self._debug = kwargs.pop('debug', False)
        host, port = MongoDBDriver._host, MongoDBDriver._port
        db = 'traderiddb' if not self._debug else 'testtraderiddb'
        connect(db, host=host, port=port, alias=db)
        traderidcoll = switch(TraderIdColl, db)
        db = 'twseiddb' if not self._debug else 'testtwseiddb'
        connect(db, host=host, port=port, alias=db)
        twseidcoll = switch(TwseIdColl, db)
        kwargs = {
            'stock': {
                'coll': twseidcoll,
                'debug': self._debug,
                'opt': 'twse'
            },
            'trader': {
                'coll': traderidcoll,
                'debug': self._debug,
                'opt': 'twse'
            }
        }
        self._stock = StockIdDBHandler(**kwargs['stock'])
        self._trader = TraderIdDBHandler(**kwargs['trader'])

    @property
    def stock(self):
        return self._stock

    @property
    def trader(self):
        return self._trader


class OtcIdDBHandler(TwseIdDBHandler):

    def __init__(self, **kwargs):
        super(OtcIdDBHandler, self).__init__(**copy.deepcopy(kwargs))
        self._debug = kwargs.pop('debug', False)
        host, port = MongoDBDriver._host, MongoDBDriver._port
        db = 'traderiddb' if not self._debug else 'testtraderiddb'
        connect(db, host=host, port=port, alias=db)
        traderidcoll = switch(TraderIdColl, db)
        db = 'otciddb' if not self._debug else 'testotciddb'
        connect(db, host=host, port=port, alias=db)
        otcidcoll = switch(OtcIdColl, db)
        kwargs = {
            'stock': {
                'coll': otcidcoll,
                'debug': self._debug,
                'opt': 'otc'
            },
            'trader': {
                'coll': traderidcoll,
                'debug': self._debug,
                'opt': 'otc'
            }
        }
        self._stock = StockIdDBHandler(**kwargs['stock'])
        self._trader = TraderIdDBHandler(**kwargs['trader'])


class StockIdDBHandler(object):

    def __init__(self, **kwargs):
        self._coll = kwargs.pop('coll', None)
        self._debug = kwargs.pop('debug', False)
        self._opt = kwargs.pop('opt', None)
        assert(self._coll)

    @property
    def coll(self):
        return self._coll

    def get_ids(self, limit=0):
        if self._debug:
            if self._opt == 'twse':
                for stockid in ['2317', '1314', '2330']:
                    yield stockid
            else:
                for stockid in ['5371', '1565', '3105']:
                    yield stockid
        else:
            cursor = self._coll.objects.limit(limit) if limit > 0 else self._coll.objects.all()
            cursor = list(cursor)
            for it in cursor:
                yield it.stockid

    def get_names(self, limit=0):
        if self._debug:
            if self._opt == 'twse':
                for stocknm in [u'鴻海', u'中石化', u'台積電']:
                    yield stocknm
            else:
                for stocknm in [u'中光電', u'精華', u'穩懋']:
                    yield stocknm
        else:
            cursor = self._coll.objects.limit(limit) if limit > 0 else self._coll.objects.all()
            cursor = list(cursor)
            for it in cursor:
                yield it.stocknm

    def get_id(self, stocknm):
        cursor = self._coll.objects(Q(stocknm=stocknm)).limit(1)
        cursor = list(cursor)
        if cursor:
            return cursor[0].stockid

    def get_name(self, stockid):
        cursor = self._coll.objects(Q(stockid=stockid)).limit(1)
        cursor = list(cursor)
        if cursor:
            return cursor[0].stocknm

    def has_id(self, stockid):
        cursor = self._coll.objects(Q(stockid=stockid)).limit(1)
        cursor = list(cursor)
        return True if cursor else False

    def has_name(self, stocknm):
        cursor = self._coll.objects(Q(stocknm=stocknm)).limit(1)
        cursor = list(cursor)
        return True if cursor else False

    def is_warrant(self, stockid):
        return len(stockid) >= 6

    def update_raw(self, item):
        self.insert_raw(item)

    def delete_raw(self, item):
        pass

    def insert_raw(self, item):
        keys = [k for k,v in StockIdColl._fields.iteritems()]
        for it in item:
            cursor = self._coll.objects(Q(stockid=it['stockid']))
            cursor = list(cursor)
            coll = self._coll() if len(cursor) == 0 else cursor[0]
            [setattr(coll, k, it[k]) for k in keys]
            coll.save()

class TraderIdDBHandler(object):

    def __init__(self, **kwargs):
        self._coll = kwargs.pop('coll', None)
        self._debug = kwargs.pop('debug', False)
        self._opt = kwargs.pop('opt', None)
        assert(self._coll)

    @property
    def coll(self):
        return self._coll

    def get_ids(self, limit=0):
        if self._debug:
            if self._opt in ['twse', 'otc']:
                for traderid in ['1590', '1440', '1470']:
                    yield traderid
        else:
            cursor = self._coll.objects.limit(limit) if limit > 0 else self._coll.objects.all()
            cursor = list(cursor)
            for it in cursor:
                yield it.traderid

    def get_names(self, limit=0):
        if self._debug:
            if self._opt in ['twse', 'otc']:
                for tradernm in [u'花旗環球', u'美林', u'台灣摩根']:
                    yield tradernm
        else:
            cursor = self._coll.objects.limit(limit) if limit > 0 else self._coll.objects.all()
            cursor = list(cursor)
            for it in cursor:
                yield it.tradernm

    def get_id(self, tradernm):
        cursor = self._coll.objects(Q(tradernm=tradernm)).limit(1)
        cursor = list(cursor)
        if cursor:
            return cursor[0].traderid

    def get_name(self, traderid):
        cursor = self._coll.objects(Q(traderid=traderid)).limit(1)
        cursor = list(cursor)
        if cursor:
            return cursor[0].tradernm

    def has_id(self, traderid):
        cursor = self._coll.objects(Q(traderid=traderid)).limit(1)
        cursor = list(cursor)
        return True if cursor else False

    def has_name(self, tradernm):
        cursor = self._coll.objects(Q(tradernm=tradernm)).limit(1)
        cursor = list(cursor)
        return True if cursor else False

    def update_raw(self, item):
        self.insert_raw(item)

    def delete_raw(self, item):
        pass

    def insert_raw(self, item):
        keys = [k for k,v in TraderIdColl._fields.iteritems()]
        for it in item:
            cursor = self._coll.objects(Q(traderid=it['traderid']))
            cursor = list(cursor)
            coll = self._coll() if len(cursor) == 0 else cursor[0]
            [setattr(coll, k, it[k]) for k in keys]
            coll.save()