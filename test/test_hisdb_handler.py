# -*- coding: utf-8 -*-

import unittest
import time
import threading
from datetime import datetime, timedelta

from test.test_start import TestBase, TestTwseHisAll
from handler.hisdb_handler import *
from handler.iddb_handler import *

# djano test
import django
from django.template import Context, Template
from django.conf import settings

settings.configure(
        USE_TZ=True,
        INSTALLED_APPS=('django.contrib.auth', 'mongoengine.django.mongo_auth'),
        AUTH_USER_MODEL=('mongo_auth.MongoUser'),
        AUTHENTICATION_BACKENDS = ('mongoengine.django.auth.MongoEngineBackend',)
)


class TestTwseHisDBTraderQuery(TestTwseHisAll):

    def setUp(self):
        super(TestTwseHisDBTraderQuery, self).setUp()
        self._assert_threading_query_start()

    def tearDown(self):
        self._assert_threading_query_join()
        super(TestTwseHisDBTraderQuery, self).tearDown()

    def test_on_run(self):
        # make sure thread querying has completed
        time.sleep(2)

    def _assert_threading_query_start(self):
        self._check = True
        self._pool = []
        starttime = datetime.utcnow() - timedelta(days=4)
        endtime = datetime.utcnow()
        self._db = TwseHisDBHandler()
        cursor = self._db.trader.query(starttime, endtime, ['2330'], [], 'stock', 'totalvolume', 3)
        self._traderids = self._db.trader.map_alias(['2330'], 'stock', ['top0'])
        # update handler as new ptr
        self._db = TwseHisDBHandler()

        def wap_get_toptrader_data(starttime, endtime, traderids):
            while self._check:
                cursor = self._db.trader.query(starttime, endtime, [], traderids, 'trader', 'totalvolume', 3)
                if cursor:
                    if len(self._pool) > 3:
                        self._pool.pop(0)
                    self._pool.append(cursor)
                self._db.trader.drop()
                time.sleep(0.5)

        self._threads = [
            threading.Thread(
                target=wap_get_toptrader_data,
                args=(starttime, endtime, self._traderids))
            ]

        [it.setDaemon(True) for it in self._threads]
        [it.start() for it in self._threads]

    def _assert_threading_query_join(self):
        self._check = False
        stream = self._db.trader.to_pandas(self._pool[-1])
        print stream


class TestTwseHisDBStockQuery(TestTwseHisAll):

    def setUp(self):
        super(TestTwseHisDBStockQuery, self).setUp()
        self._assert_threading_query_start()

    def tearDown(self):
        self._assert_threading_query_join()
        super(TestTwseHisDBStockQuery, self).tearDown()

    def test_on_run(self):
        # make sure thread querying has completed
        time.sleep(2)

    def _assert_threading_query_start(self):
        self._check = True
        self._pool = []
        starttime = datetime.utcnow() - timedelta(days=4)
        endtime = datetime.utcnow()
        self._db = TwseHisDBHandler()
        self._id = TwseIdDBHandler()
        self._stockids = list(self._id.stock.get_ids(debug=True, opt='twse'))

        def wap_get_stock_data(starttime, endtime, stockids):
            while self._check:
                cursor = self._db.stock.query(starttime, endtime, stockids)
                if cursor:
                    if len(self._pool) > 3:
                        self._pool.pop(0)
                    self._pool.append(cursor)
                time.sleep(0.5)

        self._threads = [
            threading.Thread(
                target=wap_get_stock_data,
                args=(starttime, endtime, self._stockids))
            ]

        [it.setDaemon(True) for it in self._threads]
        [it.start() for it in self._threads]

    def _assert_threading_query_join(self):
        self._check = False
        [it.join() for it in self._threads]
        stream = self._db.stock.to_pandas(self._pool[-1])
        print stream


class TestTwseHisDBAllQuery(TestTwseHisAll):

    def setUp(self):
        super(TestTwseHisDBAllQuery, self).setUp()
        self._assert_threading_query_start()

    def tearDown(self):
        self._assert_threading_query_join()
        super(TestTwseHisDBAllQuery, self).tearDown()

    def test_on_run(self):
        # make sure thread querying has completed
        time.sleep(2)

    def _assert_threading_query_start(self):
        self._check = True
        self._pool = []
        starttime = datetime.utcnow() - timedelta(days=4)
        endtime = datetime.utcnow()
        self._db = TwseHisDBHandler()
        self._id = TwseIdDBHandler()
        self._stockids = list(self._id.stock.get_ids(debug=True, opt='twse'))

        def wap_get_all_data(starttime, endtime, stockids):
            while self._check:
                stream = self._db.transform_all_data(starttime, endtime, stockids, [], 'totalvolume', 10)
                if not stream.empty:
                    if len(self._pool) > 3:
                        self._pool.pop(0)
                    self._pool.append(stream)
                time.sleep(0.5)

        self._threads = [
            threading.Thread(
                target=wap_get_all_data,
                args=(starttime, endtime, self._stockids))
        ]

        [it.setDaemon(True) for it in self._threads]
        [it.start() for it in self._threads]

    def _assert_threading_query_join(self):
        self._check = False
        [it.join() for it in self._threads]
        stream = self._pool[-1]
        for stockid in self._stockids:
            print stream[stockid]


if __name__ == '__main__':
    unittest.main()
