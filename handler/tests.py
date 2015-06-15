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
    'TestTwseHisFrameQuery': False,
    'TestTwseHisItemJoin': False,
    'TestTwseHisItemParallel': False,
    'TestTwseHisItemRouter': False
}

@unittest.skipIf(skip_tests['TestTwseHisItemQuery'], "skip")
class TestTwseHisItemQuery(NoSQLTestCase):

    def test_on_run(self):
        kwargs = {
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'traderids': [],
            'opt': 'twse',
            'algorithm': None,
            'debug': True
        }
        collect = create_hiscollect(**kwargs)
        for k in ['hisstock', 'hiscredit', 'histrader']:
            collect['frame'][k].update({'on': True })

        t = timeit.Timer()
        item, db = collect_hisitem(collect)
        self.assertTrue(item)
        for k in ['stockitem', 'traderitem', 'credititem']:
            self.assertTrue(item[k])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)

@
class TestTwseHisItemJoin(NoSQLTestCase)

@
class TestTwseHisItemParallel

@
class TestTwseHisItemRouter
    

@unittest.skipIf(skip_tests['TestTwseHisFrameQuery'], "skip")
class TestTwseHisFrameQuery(NoSQLTestCase):

    def test_on_run(self):
        kwargs = {
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'traderids': [],
            'opt': 'twse',
            'algorithm': None,
            'debug': True
        }
        collect = create_hiscollect(**kwargs)
        for k in ['hisstock', 'hiscredit', 'histrader']:
            collect['frame'][k].update({'on': True })

        t = timeit.Timer()
        panel, db = collect_hisframe(collect)
        self.assertTrue(panel is not None)
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)
        for k in ['open', 'high', 'low', 'close', 'volume', 'financeused', 'bearishused']:
            self.assertFalse(panel['2317'][k].empty)
            self.assertTrue(panel['2317'][k].sum >= 0)
        print panel['2317']
