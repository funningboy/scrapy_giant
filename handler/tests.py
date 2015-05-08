# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

#from celery import chain, group
import timeit
import unittest
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from handler.tasks import *
from django.template import Context, Template

class TestTwseHisStockQuery(NoSQLTestCase):

    def test_on_run(self):
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        t = timeit.Timer()
        args = ('twse', starttime, endtime, ['2317'], 'totalvolume', 10, True)
        panel, db = trans_hisstock.delay(*args).get()
        print "run stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)

class TestTwseHisTraderQuery(NoSQLTestCase):

    def test_on_run(self):
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()

        # stock base trans
        t = timeit.Timer()
        args = ('twse', starttime, endtime, ['2317'], [], 'stock', ['totalvolume']*3, 10, True)
        panel, db = trans_hisframe.delay(*args).get()
        tops = db.trader.get_alias(['2317'], 'trader', ["top%d" %i for i in range(10)])
        tops = {v:k for v,k in enumerate(tops)}
        print "run trader->stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)
        
        # trader base trans
        t = timeit.Timer()
        args = ('twse', starttime, endtime, [], [tops[0]], 'trader', ['totalvolume']*3, 10, True)
        panel, db = trans_hisframe.delay(*args).get()
        print "run trader->trader 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel[tops[0]].empty)

class TestOtcHisStockQuery(NoSQLTestCase):

    def test_on_run(self):
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        t = timeit.Timer()
        args = ('otc', starttime, endtime, ['5371'], 'totalvolume', 10, True)
        panel, db = trans_hisstock.delay(*args).get()
        print "run stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['5371'].empty)

class TestOtcHisTraderQuery(NoSQLTestCase):

    def test_on_run(self):
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        
        # stock base trans
        t = timeit.Timer()
        args = ('otc', starttime, endtime, ['5371'], [], 'stock', 'totalvolume', 10, True)
        panel, db = trans_histoptrader(*args)
        tops = db.trader.get_alias(['5371'], 'stock', ["top%d" %i for i in range(10)])
        tops = {v:k for v,k in enumerate(tops)}
        print "run trader->stock 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['5371'].empty)
        
        # trader base trans
        t = timeit.Timer()
        args = ('otc', starttime, endtime, [], [tops[0]], 'trader', 'totalvolume', 10, True)
        panel, db = trans_histoptrader(*args)
        print "run trader->trader 10d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel[tops[0]].empty)

