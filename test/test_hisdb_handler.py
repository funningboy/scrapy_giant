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
        kwargs = []
        for i in range(3):
            kwargs.append({
                'debug': True,
                'opt': 'twse'
            })
        self._db = TwseHisDBHandler(**kwargs[0])
        self._id = TwseIdDBHandler(**kwargs[1])
        args = (starttime, endtime, ['2330'], [], 'stock', 'totalvolume', 10)
        cursor = self._db.trader.query_raw(*args)
        cursor = list(cursor)
        tops = self._db.trader.get_alias(['2330'], 'trader', ['top0'])
        # update handler as new
        self._db = TwseHisDBHandler(**kwargs[2])

        def wap_get_toptrader_data():
            while self._check:
                args = (starttime, endtime, ['2330'], [tops[0]], 'trader', 'totalvolume', 10)
                cursor = self._db.trader.query_raw(*args)
                if cursor:
                    if len(self._pool) > 3:
                        self._pool.pop(0)
                    self._pool.append(cursor)
                time.sleep(0.5)

        self._threads = [
            threading.Thread(
                target=wap_get_toptrader_data)
            ]

        [it.setDaemon(True) for it in self._threads]
        [it.start() for it in self._threads]

    def _assert_threading_query_join(self):
        self._check = False
        [it.join() for it in self._threads]
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
        kwargs = []
        for i in range(2):
            kwargs.append({
                'debug': True,
                'opt': 'twse'
            })
        self._db = TwseHisDBHandler(**kwargs[0])
        self._id = TwseIdDBHandler(**kwargs[1])

        def wap_get_stock_data():
            while self._check:
                args = (starttime, endtime, ['2330'], 'totalvolume', 10)
                cursor = self._db.stock.query_raw(*args)
                if cursor:
                    if len(self._pool) > 3:
                        self._pool.pop(0)
                    self._pool.append(cursor)
                time.sleep(0.5)

        self._threads = [
            threading.Thread(
                target=wap_get_stock_data)
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
        kwargs = []
        for i in range(3):
            kwargs.append({
                'debug': True,
                'opt': 'twse'
            })
        self._db = TwseHisDBHandler(**kwargs[0])
        self._id = TwseIdDBHandler(**kwargs[1])
        args = (starttime, endtime, ['2330'], [], 'stock', 'totalvolume', 10)
        cursor = self._db.trader.query_raw(*args)
        cursor = list(cursor)
        tops = self._db.trader.get_alias(['2330'], 'trader', ['top0'])
        # update handler as new
        self._db = TwseHisDBHandler(**kwargs[2])

        def wap_get_all_data():
            while self._check:
                args = (starttime, endtime, ['2330'], [tops[0]], ['totalvolume']*3, 10)
                stream = self._db.transform_all_data(*args)
                if not stream.empty:
                    if len(self._pool) > 3:
                        self._pool.pop(0)
                    self._pool.append(stream)
                time.sleep(0.5)

        self._threads = [
            threading.Thread(
                target=wap_get_all_data)
        ]

        [it.setDaemon(True) for it in self._threads]
        [it.start() for it in self._threads]

    def _assert_threading_query_join(self):
        self._check = False
        [it.join() for it in self._threads]
        print self._pool[-1]


if __name__ == '__main__':
    unittest.main()
