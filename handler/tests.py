# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

import timeit
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from bin.tests import *
from handler.tasks import *
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler

from django.template import Context, Template

class TestTwseHisStockQuery(TestTwseHisTrader, TestTwseHisStock):

    def test_on_run(self):
        super(TestTwseHisStockQuery, self).test_on_run()
        t = timeit.Timer()
        starttime = datetime.utcnow() - timedelta(days=4)
        endtime = datetime.utcnow()
        args = ('twse', starttime, endtime, ['2317'])
        panel = run_hisstock_query.delay(*args).get()
        print "run stock 300d query using %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)


class TestTwseHisTraderQuery(TestTwseHisTrader, TestTwseHisStock):

    def test_on_run(self):
        super(TestTwseHisTrader, self).test_on_run()
        t = timeit.Timer()
        starttime = datetime.utcnow() - timedelta(days=300)
        endtime = datetime.utcnow()
        args = ('twse', starttime, endtime, ['2317'], [], 'stock', 'buy', 10)
        panel = run_histoptrader_query.delay(*args).get()
        print "run stock 300d query using %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)
