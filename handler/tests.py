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

class TestTwseHisTraderQuery(NoSQLTestCase):

    def test_on_run(self):
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        stockid = '2317'
        limit = 10
        collect = {
            'debug': True,
            'opt': 'twse',
            'frame': {
                # hisstock frame collect
                'hisstock': {
                    'starttime': starttime,
                    'endtime': endtime,
                    'stockids': [stockid],
                    'order': 'totalvolume',
                    'limit': limit
                },
                # histrader frame collect
                'histrader': {
                    'starttime': starttime,
                    'endtime': endtime,
                    'stockids': [stockid],
                    'traderids':[],
                    'base': 'stock',
                    'order': 'totalvolume',
                    'limit': limit
                },
                # hiscredit frame collect
                'hiscredit': {
                    'starttime': starttime,
                    'endtime': endtime,
                    'stockids': [stockid],
                    'order': 'decfinance',
                    'limit': limit
                }
            }
        }
        t = timeit.Timer()
        panel, db = collect_hisframe(**collect)
        self.assertTrue(panel is not None)
        self.assertFalse(panel.empty)
        self.assertFalse(panel[stockid].empty)
        for k in ['open', 'high', 'low', 'close', 'volume']:
            self.assertFalse(self.panel[stockid][k].empty)

class TestOtcHisTraderQuery(NoSQLTestCase):

    def test_on_run(self):
        pass
