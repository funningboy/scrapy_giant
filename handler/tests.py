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

skip_tests = {
    'TestTwseHisItemQuery': False,
    'TestTwseHisFrameQuery': False
}

@unittest.skipIf(skip_tests['TestTwseHisItemQuery'], "skip")
class TestTwseHisItemQuery(NoSQLTestCase):

    def test_on_run(self):
        starttime = datetime.utcnow() - timedelta(days=3)
        endtime = datetime.utcnow()
        stockid = '2317'
        limit = 10
        collect = {
            'debug': True,
            'opt': 'twse',
            'frame': {
                # hisstock item collect
                'hisstock': {
                    'starttime': starttime,
                    'endtime': endtime,
                    'stockids': [stockid],
                    'base': 'stock',
                    'order': ['-totalvolume', '-totaldiff'],
                    'callback': None,
                    'limit': limit,
                    'priority': 1
                },
                # histrader iteme collect
                'histrader': {
                    'starttime': starttime,
                    'endtime': endtime,
                    'stockids': [stockid],
                    'traderids':[],
                    'base': 'stock',
                    'order': ['-totalvolume'],
                    'callback': None,
                    'limit': limit,
                    'priority': 0
                },
                # hiscredit item collect
                'hiscredit': {
                    'starttime': starttime,
                    'endtime': endtime,
                    'stockids': [stockid],
                    'base': 'stock',
                    'order': ['-financeused', '-bearishused'],
                    'callback': None,
                    'limit': limit,
                    'priority': 2
                }
            }
        }
        t = timeit.Timer()
        item, db = collect_hisitem(**collect)
        self.assertTrue(item)
        for k in ['stockitem', 'traderitem', 'credititem']:
            self.assertTrue(item[k])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)


@unittest.skipIf(skip_tests['TestTwseHisFrameQuery'], "skip")
class TestTwseHisFrameQuery(NoSQLTestCase):
    """ makre sure db contains the data """

    def test_on_run(self):
        starttime = datetime.utcnow() - timedelta(days=3)
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
                    'base': 'stock',
                    'order': ['-totalvolume', '-totaldiff'],
                    'callback': 'to_pandas',
                    'limit': limit
                },
                # histrader frame collect
                'histrader': {
                    'starttime': starttime,
                    'endtime': endtime,
                    'stockids': [stockid],
                    'traderids':[],
                    'base': 'stock',
                    'order': ['-totalvolume', '-totalbuyvolume', '+totalsellvolume'],
                    'callback': 'to_pandas',
                    'limit': limit
                },
                # hiscredit frame collect
                'hiscredit': {
                    'starttime': starttime,
                    'endtime': endtime,
                    'stockids': [stockid],
                    'base': 'stock',
                    'order': ['-financeused', '-bearishused'],
                    'callback': 'to_pandas',
                    'limit': limit
                }
            }
        }
        t = timeit.Timer()
        panel, db = collect_hisframe(**collect)
        self.assertTrue(panel is not None)
        self.assertFalse(panel.empty)
        self.assertFalse(panel[stockid].empty)
        for k in ['open', 'high', 'low', 'close', 'volume', 'financeused', 'bearishused']:
            self.assertFalse(panel[stockid][k].empty)
        print panel['2317']
