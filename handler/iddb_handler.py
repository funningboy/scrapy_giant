
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

from mongoengine import *
from bin.start import switch
from bin.mongodb_driver import MongoDBDriver
from handler.models import TwseIdColl, OtcIdColl, TraderIdColl

__all__ = ['TwseIdDBHandler', 'OtcIdDBHandler', 'TraderIdDBHandler']


class TwseIdDBHandler(object):

    def __init__(self):
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('traderiddb', host=host, port=port, alias='traderiddb')
        traderidcoll = switch(TraderIdColl, 'traderiddb')
        connect('twseiddb', host=host, port=port, alias='twseiddb')
        twseidcoll = switch(TwseIdColl, 'twseiddb')
        self._stock = StockIdDBHandler(twseidcoll)
        self._trader = TraderIdDBHandler(traderidcoll)

    @property
    def stock(self):
        return self._stock

    @property
    def trader(self):
        return self._trader


class OtcIdDBHandler(TwseIdDBHandler):

    def __init__(self):
        super(OtcIdDBHandler, self).__init__()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('traderiddb', host=host, port=port, alias='traderiddb')
        traderidcoll = switch(TraderIdColl, 'traderiddb')
        connect('otciddb', host=host, port=port, alias='otciddb')
        otcidcoll = switch(OtcIdColl, 'otciddb')
        self._stock = StockIdDBHandler(otcidcoll)
        self._trader = TraderIdDBHandler(traderidcoll)


class StockIdDBHandler(object):

    def __init__(self, coll):
        self._coll = coll

    def get_ids(self, limit=0, debug=False, opt='twse'):
        if debug:
            if opt == 'twse':
                for stockid in ['2317', '1314', '2330']:
                    yield stockid
            else:
                for stockid in ['5371', '1565', '3105']:
                    yield stockid
        else:
            cursor = self._coll.objects.limit(limit) if limit > 0 else self._coll.objects
            cursor = list(cursor)
            for it in cursor:
                yield it.stockid

    def get_names(self, limit=0, debug=False, opt='twse'):
        if debug:
            if opt == 'twse':
                for stocknm in [u'鴻海', u'中石化', u'台積電']:
                    yield stocknm
            else:
                for stocknm in [u'中光電', u'精華', u'穩懋']:
                    yield stocknm
        else:
            cursor = self._coll.objects.limit(limit) if limit > 0 else self._coll.objects
            cursor = list(cursor)
            for it in cursor:
                yield it.stocknm

    def get_id(self, stocknm):
        cursor = self._coll.objects(Q(stocknm=stocknm)).limit(1)
        cursor = list(cursor)
        try:
            return cursor[0].stockid
        except:
            pass

    def get_name(self, stockid):
        cursor = self._coll.objects(Q(stockid=stockid)).limit(1)
        cursor = list(cursor)
        try:
            return cursor[0].stocknm
        except:
            pass

    def has_id(self, stockid):
        cursor = self._coll.objects(Q(stockid=stockid)).limit(1)
        cursor = list(cursor)
        return True if cursor else False

    def has_name(self, stocknm):
        cursor = self._coll.objects(Q(stocknm=stocknm)).limit(1)
        cursor = list(cursor)
        return True if cursor else False

    def insert(self, item):
        for it in item:
            cursor = self._coll.objects(Q(stockid=it['stockid']))
            cursor = list(cursor)
            if len(cursor) == 0:
                coll = self._coll().save()
            else:
                coll = cursor[0]
            coll.stockid = it['stockid']
            coll.stocknm = it['stocknm']
            coll.onmarket = it['onmarket']
            coll.industry = it['industry']
            coll.save()


class TraderIdDBHandler(object):

    def __init__(self, coll):
        self._coll = coll

    def get_ids(self, limit=0, debug=False, opt='twse'):
        if debug:
            if opt in ['twse', 'otc']:
                for traderid in ['1590', '1440', '1470']:
                    yield traderid
        else:
            cursor = self._coll.objects.limit(limit)
            cursor = list(cursor)
            for it in cursor:
                yield it.traderid

    def get_names(self, limit=0, debug=False, opt='twse'):
        if debug:
            if opt in ['twse', 'otc']:
                for tradernm in [u'花旗環球', u'美林', u'台灣摩根']:
                    yield tradernm
        else:
            cursor = self._coll.objects.limit(limit) if limit > 0 else self._coll.objects
            cursor = list(cursor)
            for it in cursor:
                yield it.tradernm

    def get_id(self, tradernm):
        cursor = self._coll.objects(Q(tradernm=tradernm)).limit(1)
        cursor = list(cursor)
        try:
            return cursor[0].traderid
        except:
            pass

    def get_name(self, traderid):
        cursor = self._coll.objects(Q(traderid=traderid)).limit(1)
        cursor = list(cursor)
        try:
            return cursor[0].tradernm
        except:
            pass

    def has_id(self, traderid):
        cursor = self._coll.objects(Q(traderid=traderid)).limit(1)
        cursor = list(cursor)
        return True if cursor else False

    def has_name(self, tradernm):
        cursor = self._coll.objects(Q(tradernm=tradernm)).limit(1)
        cursor = list(cursor)
        return True if cursor else False

    def insert(self, item):
        for it in item:
            cursor = self._coll.objects(Q(traderid=it['traderid']))
            cursor = list(cursor)
            if len(cursor) == 0:
                coll = self._coll().save()
            else:
                coll = cursor[0]
            coll.traderid = it['traderid']
            coll.tradernm = it['tradernm']
            coll.save()
