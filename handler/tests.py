# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

#from celery import chain, group
import timeit
import unittest
import json
from bson import json_util
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from handler.tasks import *
from handler.collects import create_hiscollect
from django.template import Context, Template

skip_tests = {
    'TestTwseHisItemQuery': False,
    'TestTwseHisFrameQuery': False
}

@unittest.skipIf(skip_tests['TestTwseHisItemQuery'], "skip")
class TestTwseHisItemQuery(NoSQLTestCase):

    def test_on_stock(self):
        kwargs = {
            'opt': 'twse',
            'targets': ['stock'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330'],
            'base': 'stock',
            'order': ['-totalvolume', '-totaldiff'],
            'callback': None,
            'limit': 1,
            'debug': True
        }
        item = collect_hisitem.delay(**kwargs).get()
        self.assertTrue(item)
        self.assertTrue(item['stockitem'])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)

    def test_on_trader(self):
        kwargs = {
            'opt': 'twse',
            'targets': ['trader'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330'],
            'base': 'stock',
            'order': ['-totalvolume'],
            'callback': None,
            'limit': 1,
            'debug': True
        }
        item = collect_hisitem.delay(**kwargs).get()
        self.assertTrue(item)
        self.assertTrue(item['traderitem'])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)

    def test_on_credit(self):
        pass

    def test_on_future(self):
        pass

    def test_on_all(self):
        kwargs = {
            'opt': 'twse',
            'targets': ['stock', 'trader', 'future', 'credit'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330'],
            'traderids': [],
            'base': 'stock',
            'order': [],
            'callback': None,
            'limit': 2,
            'debug': True
        }
        item = collect_hisitem.delay(**kwargs).get()
        self.assertTrue(item)
        [self.assertTrue(item[i]) for i in ['stockitem', 'traderitem', 'credititem', 'futureitem']] 
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)


@unittest.skipIf(skip_tests['TestTwseHisFrameQuery'], "skip")
class TestTwseHisFrameQuery(NoSQLTestCase):

    def test_on_all(self):
        kwargs = {
            'opt': 'twse',
            'targets': ['stock', 'trader', 'future', 'credit'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'traderids': [],
            'base': 'stock',
            'order': [],
            'callback': None,
            'limit': 1,
            'debug': True
        }
        panel, _ = collect_hisframe(**kwargs)
        self.assertTrue(panel is not None)
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)
        for k in ['open', 'high', 'low', 'close', 'volume', 'financeused', 'bearishused']:
            self.assertFalse(panel['2317'][k].empty)
            self.assertTrue(panel['2317'][k].sum >= 0)
        print panel['2317']
