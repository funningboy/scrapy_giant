# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

#from celery import chain, group
import timeit
import unittest
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from bin.tests import TestTwseHisTrader2, TestTwseHisStock, TestOtcHisTrader2, TestOtcHisStock, TestTraderId
from handler.tasks import *
from handler.models import StockMapColl, TraderMapColl

from django.template import Context, Template

class TestTwseHisStockQuery(TestTwseHisTrader2, TestTwseHisStock):

    def test_on_run(self):
        super(TestTwseHisStockQuery, self).test_on_run()
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        t = timeit.Timer()
        args = ('twse', starttime, endtime, ['2317'], 'totalvolume', 10)
        panel, dbhandler = trans_hisstock(*args)
        print "run stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)

class TestTwseHisTraderQuery(TestTwseHisTrader2, TestTwseHisStock):

    def test_on_run(self):
        super(TestTwseHisTraderQuery, self).test_on_run()
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        t = timeit.Timer()
        # stock base trans
        args = ('twse', starttime, endtime, ['2317'], [], 'stock', 'totalvolume', 10)
        panel, dbhandler = trans_histoptrader(*args)
        tops = dbhandler.trader.map_alias(['2317'], 'stock', ["top%d" %i for i in range(10)])
        tops = {v:k for v,k in enumerate(tops)}
        print "run trader->stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)
        # trade base trans
        t = timeit.Timer()
        args = ('twse', starttime, endtime, [], [top[0]], 'trader', 'totalvolume', 10)
        panel, dbhandler = trans_histoptrader(*args)
        print "run trader->trader 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel[top[0]].empty)

class TestOtcHisStockQuery(TestOtcHisTrader2, TestOtcHisStock):

    def test_on_run(self):
        super(TestOtcHisStockQuery, self).test_on_run()
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        t = timeit.Timer()
        args = ('otc', starttime, endtime, ['5371'])
        panel, dbhandler = trans_hisstock(*args)
        print "run stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['5371'].empty)

class TestOtcHisTraderQuery(TestOtcHisTrader2, TestOtcHisStock):

    def test_on_run(self):
        super(TestOtcHisTraderQuery, self).test_on_run()
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        t = timeit.Timer()
        # stock base trans
        args = ('otc', starttime, endtime, ['5371'], [], 'stock', 'totalvolume', 10)
        panel, dbhandler = trans_histoptrader(*args)
        tops = dbhandler.trader.map_alias(['5371'], 'stock', ["top%d" %i for i in range(10)])
        tops = {v:k for v,k in enumerate(tops)}
        print "run trader->stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['5371'].empty)
        # trader base trans
        t = timeit.Timer()
        args = ('otc', starttime, endtime, [], [tops[0]], 'trader', 'totalvolume', 10)
        panel, dbhandler = trans_histoptrader(*args)
        print "run trader->trader 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel[tops[0]].empty)

