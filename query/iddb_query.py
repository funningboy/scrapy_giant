
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

from bin.mongodb_driver import *
from bin.logger import Logger

__all__ = ['TwseIdDBQuery', 'OtcIdDBQuery']

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

    def get_stocknms(self, limit=0):
        cursor = self._coll.find().limit(limit)
        stocknms = [it['stocknm'] for it in cursor]
        for stocknm in stocknms:
            yield stocknm

    def get_industrys(self):
        raise NotImplementedError

    def get_stockid(self, stocknm):
        cursor = self._coll.find({'stocknm': stocknm})
        try:
            return list(cursor)[0]['stockid']
        except:
            return None

    def get_stocknm(self, stockid):
        cursor = self._coll.find({'stockid': stockid})
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


class TraderIDDBQuery():
    pass
