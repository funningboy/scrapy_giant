# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

import unittest
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from algorithm.tasks import *

skip_tests = {
    'TestTwseDualemaAlg': False
}

@unittest.skipIf(skip_tests['TestTwseDualemaAlg'], "skip")
class TestTwseDualemaAlg(NoSQLTestCase):

    def test_on_to_detail(self):
        kwargs = {
            'opt': 'twse',
            'targets': ['dualema'],
            'starttime': datetime.utcnow() - timedelta(days=150),
            'endtime': datetime.utcnow(),
            'base': 'stock',
            'stockids': ['2317', '2330', '1314'],
            'order': ['-portfolio_value', '-buys', '-sells'],
            'limit': 3,
            'callback': 'to_detail',
            'debug': True,
            'cfg': {
                "buf_win": 30,
                "short_ema_win": 20,
                "long_ema_win": 40
            }
        }  
        item = run_algitem.delay(**kwargs).get()
        self.assertTrue(item)
        self.assertTrue(item['dualemaitem'])  
        self.assertTrue(len(item['dualemaitem'])>0)
        self.assertTrue(set(sorted(list(item['dualemaitem'][0].keys()))) >= set(sorted(['date', 'portfolio_value', 'buy', 'open'])))
    
    def test_on_to_summary(self):
        kwargs = {
            'opt': 'twse',
            'targets': ['dualema'],
            'starttime': datetime.utcnow() - timedelta(days=150),
            'endtime': datetime.utcnow(),
            'base': 'stock',
            'stockids': ['2317', '2330', '1314'],
            'order': ['-portfolio_value', '-buys', '-sells'],
            'limit': 3,
            'callback': 'insert_summary',
            'debug': True,
            'cfg': {
                "buf_win": 30,
                "short_ema_win": 20,
                "long_ema_win": 40
            }
        } 
        alg = algdb_tasks['twse']['dualema'](**kwargs) 
        alg.sumycoll.drop_collection()
        run_algitem.delay(**kwargs).get()
        # query summary back and check
        starttime, endtime = datetime.utcnow() - timedelta(days=1), datetime.utcnow()
        if endtime.isoweekday() in [6, 7]:
            starttime -= timedelta(days=2)
        kwargs = {
            'opt': 'twse',
            'targets': ['dualema'],
            'starttime': starttime,
            'endtime': endtime,
            'base': 'stcok',
            'stockids': ['2317', '2330', '1314'],
            'order': ['-totalportfolio', '-totalbuys', '-totalsells'],
            'limit': 1,
            'debug': True,
            'cfg': {
                "buf_win": 30,
                "short_ema_win": 20,
                "long_ema_win": 40
            }
        } 
        item = collect_algitem.delay(**kwargs).get()
        self.assertTrue(item)
        self.assertTrue(item['dualemaitem'])
        self.assertTrue(len(item['dualemaitem'])>0)
        self.assertTrue(set(sorted(list(item['dualemaitem'][0].keys()))) >= set(sorted(['watchtime', 'totalportfolio', 'totalbuys'])))
