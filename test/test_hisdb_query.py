# -*- coding: utf-8 -*-

import unittest
import time
import threading
import time
import json
import re
from datetime import datetime, timedelta

from test.test_start import *
from query.hisdb_query import *

class TestTwseHisDBTraderQuery(TestTwseHisAll):
    # test order 2

    def setUp(self):
        super(TestTwseHisDBTraderQuery, self).setUp()
        self._assert_threading_query_start()

    def tearDown(self):
        self._assert_threading_query_join()
        super(TestTwseHisDBTraderQuery, self).tearDown()

    def test_on_run(self):
        # make sure thread querying has completed
        time.sleep(10)

    def _assert_threading_query_start(self):
        self._check = True
        self._pool = []
        starttime = datetime.utcnow() - timedelta(days=60)
        endtime = datetime.utcnow()
        self._dbquery = TwseHisDBQuery()

        def wap_get_toptrader_data(starttime, endtime, traderids):
            while self._check:
                data = self._dbquery.get_toptrader_data(starttime, endtime, [], traderids, 'trader')
                if not data.empty:
                    if len(self._pool) > 10:
                        self._pool.pop(0)
                    self._pool.append(data)
                time.sleep(0.5)

        self._threads = [
            threading.Thread(
                target=wap_get_toptrader_data,
                args=(starttime, endtime, ['1590', '1520', '1530', '1480']))
            ]

        [it.setDaemon(True) for it in self._threads]
        [it.start() for it in self._threads]

    def _assert_threading_query_join(self):
        self._check = False
        [it.join() for it in self._threads]
        print self._pool[-1]


class TestTwseHisDBStockQuery(TestTwseHisAll):
    # test order 1

    def setUp(self):
        super(TestTwseHisDBStockQuery, self).setUp()
        self._assert_threading_query_start()

    def tearDown(self):
        self._assert_threading_query_join()
        super(TestTwseHisDBStockQuery, self).tearDown()

    def test_on_run(self):
        # make sure thread querying has completed
        time.sleep(10)

    def _assert_threading_query_start(self):
        self._check = True
        self._pool = []
        starttime = datetime.utcnow() - timedelta(days=60)
        endtime = datetime.utcnow()
        self._dbquery = TwseHisDBQuery()

        def wap_get_stock_data(starttime, endtime, stockids):
            while self._check:
                data = self._dbquery.get_stock_data(starttime, endtime, stockids)
                if not data.empty:
                    if len(self._pool) > 10:
                        self._pool.pop(0)
                    self._pool.append(data)
                time.sleep(0.5)

        self._threads = [
            threading.Thread(
                target=wap_get_stock_data,
                args=(starttime, endtime, ['2317', '2330', '2388']))
            ]

        [it.setDaemon(True) for it in self._threads]
        [it.start() for it in self._threads]

    def _assert_threading_query_join(self):
        self._check = False
        [it.join() for it in self._threads]
        print self._pool[-1]

if __name__ == '__main__':
    unittest.main()
