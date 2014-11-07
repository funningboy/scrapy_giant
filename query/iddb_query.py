
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

from bin.mongodb_driver import *
from bin.logger import Logger

__all__ = ['TwseIdDBQuery', 'OtcIdDBQuery', 'TraderIdDBQuery']

class BaseIdDBQuery(object):

    def __init__(self):
        self._client = connect_mongodb_service()
        self._db = self._client.twsedb
        self._coll = self._client.twsedb.twseidcoll
        self._coll.ensure_index([('stockid', 1), ('stocknm', 1)])

    def get_stockids(self, limit=0, debug=False):
        if debug and limit == 1:
            yield '2317'
        elif debug and limit == 0:
            for stockid in ['2317', '1314', '2330']:
                yield stockid
        else:
            cursor = self._coll.find().limit(limit)
            stockids = [it['stockid'] for it in cursor]
            for stockid in stockids:
                yield stockid

    def get_stocknms(self, limit=0, debug=False):
        if debug and limit == 1:
            yield u'鴻海'
        elif debug and limit == 0:
            for stocknm in [u'鴻海', u'中石化', u'台積電']:
                yield stocknm
        else:
            cursor = self._coll.find().limit(limit)
            stocknms = [it['stocknm'] for it in cursor]
            for stocknm in stocknms:
                yield stocknm

    def get_industrys(self):
        raise NotImplementedError

    def get_stockid(self, stocknm):
        cursor = self._coll.find({'stocknm': stocknm}).limit(1)
        try:
            return list(cursor)[0]['stockid']
        except:
            return None

    def get_stocknm(self, stockid):
        cursor = self._coll.find({'stockid': stockid}).limit(1)
        try:
            return list(cursor)[0]['stocknm']
        except:
            return None

    def set_stockid(self, item):
        for it in item:
            bulk = self._coll.initialize_ordered_bulk_op()
            bulk.find({'stockid': it['stockid']}).update({
                '$set': {
                    'stockid': it['stockid'],
                    'stocknm': it['stocknm'],
                    'onmarket': it['onmarket'],
                    'industry': it['industry']
                }
            })
            rst = bulk.execute()
            if sum([rst['nMatched'], rst['nInserted'], rst['nModified']]) == 0:
                # insert new content
                bulk = self._coll.initialize_ordered_bulk_op()
                bulk.insert({
                    'stockid': it['stockid'],
                    'stocknm': it['stocknm'],
                    'onmarket': it['onmarket'],
                    'industry': it['industry']
                })
                bulk.execute()


class TwseIdDBQuery(BaseIdDBQuery):

    def __init__(self):
        super(TwseIdDBQuery, self).__init__()
        self._db = self._client.twsedb
        self._coll = self._client.twsedb.twseidcoll
        self._coll.ensure_index([('stockid', 1), ('stocknm', 1)])


class OtcIdDBQuery(BaseIdDBQuery):

    def __init__(self):
        super(OtcIdDBQuery, self).__init__()
        self._db = self._client.otcdb
        self._coll = self._client.otcdb.otcidcoll
        self._coll.ensure_index([('stockid', 1), ('stocknm', 1)])

    def get_stockids(self, limit=0, debug=False):
        if debug and limit == 1:
            yield '5371'
        elif debug and limit == 0:
            for stockid in ['5371', '1565', '3105']:
                yield stockid
        else:
            cursor = self._coll.find().limit(limit)
            stockids = [it['stockid'] for it in cursor]
            for stockid in stockids:
                yield stockid

    def get_stocknms(self, limit=0, debug=False):
        if debug and limit == 1:
            yield u'中光電'
        elif debug and limit == 0:
            for stocknm in [u'中光電', u'精華', u'穩懋']:
                yield stocknm
        else:
            cursor = self_coll.find().limit(limit)
            stocknms = [it['stocknm'] for it in cursor]
            for stcoknm in stocknms:
                yield stocknm


class TraderIdDBQuery(object):

    def __init__(self):
        self._client = connect_mongodb_service()
        self._db = self._client.traderdb
        self._coll = self._client.traderdb.traderidcoll
        self._coll.ensure_index([('traderid', 1), ('tradernm', 1)])

    def get_traderids(self, limit=0, debug=False):
        if debug and limit == 1:
            yield '1590'
        elif debug and limit == 0:
            for traderid in ['1590', '1440', '1470']:
                yield traderid
        else:
            cursor = self._coll.find().limit(limit)
            traderids = [it['traderid'] for it in cursor]
            for traderid in traderids:
                yield traderid

    def get_tradernms(self, limit=0, debug=False):
        if debug and limit == 1:
            yield u'花旗環球'
        elif debug and limit == 0:
            for tradernm in [u'花旗環球', u'美林', u'台灣摩根']:
                yield tradernm
        else:
            cursor = self_coll.find().limit(limit)
            tradernms = [it['tradernm'] for it in cursor]
            for tradernm in tradernms:
                yield tradernm

    def get_traderid(self, tradernm):
        cursor = self._coll.find({'tradernm': stocknm}).limit(1)
        try:
            return list(cursor)[0]['traderid']
        except:
            return None

    def get_tradernm(self, traderid):
        cursor = self._coll.find({'traderid': stocknm}).limit(1)
        try:
            return list(cursor)[0]['tradernm']
        except:
            return None

    def set_traderid(self, item):
        for it in item:
            bulk = self._coll.initialize_ordered_bulk_op()
            bulk.find({'traderid': it['traderid']}).update({
                '$set': {
                    'traderid': it['traderid'],
                    'tradernm': it['tradernm'],
                }
            })
            rst = bulk.execute()
            if sum([rst['nMatched'], rst['nInserted'], rst['nModified']]) == 0:
                # insert new content
                bulk = self._coll.initialize_ordered_bulk_op()
                bulk.insert({
                    'traderid': it['traderid'],
                    'tradernm': it['tradernm'],
                })
                bulk.execute()
