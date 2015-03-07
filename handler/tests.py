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

class TestTwseHisStockQuery(TestTwseHisTrader, TestTwseHisStock):

    def test_on_run(self):
        super(TestTwseHisStockQuery, self).test_on_run()
        t = timeit.Timer()
        starttime = datetime.utcnow() - timedelta(days=4)
        endtime = datetime.utcnow()
        args = ('twse', starttime, endtime, ['2317'], 'totalvolume', 10)
        panel = chain(
            query_hisstock.s(*args),
            trans_hisstock.s()
        ).apply_async().get()
        print "run stock 300d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)

    def test_on_orm(self):
        super(TestTwseHisStockQuery, self).test_on_run()
#        response = self.client.get(reverse('proposal:proposal', kwargs={"proposal_id": "08-01-YS-01-001"}))
#        self.assertEqual(response.status_code, 200)

class TestTwseHisTraderQuery(TestTwseHisTrader, TestTwseHisStock):

    def test_on_run(self):
        super(TestTwseHisTraderQuery, self).test_on_run()
        t = timeit.Timer()
        starttime = datetime.utcnow() - timedelta(days=300)
        endtime = datetime.utcnow()
        args = ('twse', starttime, endtime, ['2317'], [], 'stock', 'totalvolume', 10)
        panel = chain(
            query_histoptrader.s(*args),
            trans_histoptrader.s()
        ).apply_async().get()
        print "run stock 300d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)

    def test_on_orm(self):
        super(TestTwseHisTraderQuery, self).test_on_run()
        pass

class TestOtcHisStockQuery(TestOtcHisTrader, TestOtcHisStock):

    def test_on_run(self):
        super(TestOtcHisStockQuery, self).test_on_run()
        t = timeit.Timer()
        starttime = datetime.utcnow() - timedelta(days=4)
        endtime = datetime.utcnow()
        args = ('otc', starttime, endtime, ['5371'])
        panel = chain(
            query_hisstock.s(*args),
            trans_hisstock.s()
        ).apply_async().get()
        print "run stock 300d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['5371'].empty)

    def test_on_orm(self):
        super(TestOtcHisStockQuery, self).test_on_run()
        pass

class TestOtcHisTraderQuery(TestOtcHisTrader, TestOtcHisStock):

    def test_on_run(self):
        super(TestOtcHisTraderQuery, self).test_on_run()
        t = timeit.Timer()
        starttime = datetime.utcnow() - timedelta(days=300)
        endtime = datetime.utcnow()
        args = ('otc', starttime, endtime, ['5371'], [], 'stock', 'totalvolume', 10)
        panel = chain(
            query_histoptrader.s(*args),
            trans_histoptrader.s()
        ).apply_async().get()
        print "run stock 300d query used %.4f(s)" % (t.timeit())
        self.assertFalse(panel.empty)
        self.assertFalse(panel['5371'].empty)

    def test_on_orm(self):
        super(TestOtcHisTraderQuery, self).test_on_run()
        pass
