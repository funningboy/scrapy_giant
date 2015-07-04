# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

import timeit
import unittest
import json
from bson import json_util
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from handler.tasks import *
from handler.collects import create_hiscollect
from django.template import Context, Template
from algorithm.algdb_handler import TwseDualemaAlg

skip_tests = {
    'TestTwseDualemaAlg': False
}

@unittest.skipIf(skip_tests['TestTwseDualemaAlg'], "skip")
class TestTwseDualemaAlg(NoSQLTestCase):

    def test_on_run(self):
        kwargs = {
            'opt': 'twse',
            'starttime': datetime.utcnow() - timedelta(days=150),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330', '1314'],
            'order': ['-portfolio_value', '-buys', '-sells'],
            'debug': True,
            'cfg': {
                "buf_win": 30,
                "short_ema_win": 20,
                "long_ema_win": 40
            }
        }  
        # as run
        alg = TwseDualemaAlg(**kwargs)
        alg.run()
        df = alg.finalize()
        self.assertTrue(df is not None)
        self.assertFalse(df.empty)
        self.assertTrue(set(sorted(list(df.index))) == set(sorted(['2317', '2330', '1314'])))
        self.assertTrue(set(sorted(list(df.columns))) >= set(sorted(['portfolio_value', 'buys', 'date', 'bufwin']))) 
        self.assertFalse(df.empty)

    def test_on_to_detail(self):
        kwargs = {
            'opt': 'twse',
            'starttime': datetime.utcnow() - timedelta(days=150),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330', '1314'],
            'order': ['-portfolio_value', '-buys', '-sells'],
            'debug': True,
            'cfg': {
                "buf_win": 30,
                "short_ema_win": 20,
                "long_ema_win": 40
            }
        }  
        alg = TwseDualemaAlg(**kwargs)
        alg.run()
        item = alg.finalize(alg.to_detail)
        self.assertTrue(len(item)>0)
        self.assertTrue(set(sorted(list(item[0].keys()))) >= set(sorted(['date', 'portfolio_value', 'buy', 'open'])))
    
    def test_on_insert_summary(self):
        # as collect/query
        alg = TwseDualemaAlg(**kwargs)
        alg.sumycoll.drop_collection()
        alg.run()
        alg.finalize(alg.insert_summary)
        starttime, endtime = datetime.utcnow() - timedelta(days=1), datetime.utcnow()
        if endtime.isoweekday() in [6, 7]:
            starttime -= timedelta(days=2)
        item = alg.query_summary(starttime=starttime, endtime=endtime)
        self.assertTrue(len(item)>0)
        self.assertTrue(set(sorted(list(item[0].keys()))) >= set(sorted(['watchtime', 'totalportfolio', 'totalbuys'])))


