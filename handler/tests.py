# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

from celery import chain
import timeit
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from bin.tests import *
from handler.tasks import *
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.models import StockMapColl, TraderMapColl

from django.template import Context, Template

class TestTwseHisStockQuery(TestTwseHisTrader2, TestTwseHisStock):

    def test_on_run(self):
        super(TestTwseHisStockQuery, self).test_on_run()
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        t = timeit.Timer()
        args = ('twse', starttime, endtime, ['2317'], 'totalvolume', 10)
        panel, dbhandler = trans_hisstock.delay(*args).get()
        print "run stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)


class TestTwseHisTraderQuery(TestTwseHisTrader2, TestTwseHisStock):

    def test_on_run(self):
        super(TestTwseHisTraderQuery, self).test_on_run()
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        t = timeit.Timer()
        args = ('twse', starttime, endtime, ['2317'], [], 'stock', 'totalvolume', 10)
        panel, dbhandler = trans_histoptrader.delay(*args).get()
        tops = dbhandler.trader.map_alias(['2317'], 'stock', ["top%d" %i for i in range(10)])
        tops = {v:k for v,k in enumerate(tops)}
        traderid = tops[0]
        print "run trader->stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)

        t = timeit.Timer()
        args = ('twse', starttime, endtime, [], [traderid], 'trader', 'totalvolume', 10)
        panel, dbhandler = trans_histoptrader.delay(*args).get()
        print "run trader->trader 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel[traderid].empty)


class TestOtcHisStockQuery(TestOtcHisTrader2, TestOtcHisStock):

    def test_on_run(self):
        super(TestOtcHisStockQuery, self).test_on_run()
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        t = timeit.Timer()
        args = ('otc', starttime, endtime, ['5371'])
        print "run stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['5371'].empty)


class TestOtcHisTraderQuery(TestOtcHisTrader2, TestOtcHisStock):

    def test_on_run(self):
        super(TestOtcHisTraderQuery, self).test_on_run()
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        t = timeit.Timer()
        args = ('otc', starttime, endtime, ['5371'], [], 'stock', 'totalvolume', 10)
        panel, dbhandler = trans_histoptrader.delay(*args).get()
        tops = dbhandler.trader.map_alias(['5371'], 'stock', ["top%d" %i for i in range(10)])
        tops = {v:k for v,k in enumerate(tops)}
        traderid = tops[0]
        print "run trader->stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['5371'].empty)

        t = timeit.Timer()
        args = ('twse', starttime, endtime, [], [traderid], 'trader', 'totalvolume', 10)
        panel, dbhandler = trans_histoptrader.delay(*args).get()
        print "run trader->trader 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel[traderid].empty)

