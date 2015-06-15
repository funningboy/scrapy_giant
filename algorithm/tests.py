# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

import timeit
import unittest
import json
from bson import json_util
import copy
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from handler.tasks import *
from handler.collects import create_hiscollect
from django.template import Context, Template
from algorithm.algdb_handler import TwseDualemaAlg

skip_tests = {
    'TestTwseDualemaAlg': False,
}

class TestTwseDualemaAlg(NoSQLTestCase):

    def setUp(self):
        self._kwargs = {
            'starttime': datetime.utcnow() - timedelta(days=10),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330', '1314'],
            'traderids': [],
            'opt': 'twse',
            'algorithm': None,
            'debug': True
        }   

    def test_on_run(self):
        alg = TwseDualemaAlg(**copy.deepcopy(self._kwargs))
        panel = alg.run()
        self.assertTrue(panel is not None)
        self.assertFalse(panel.empty)
        self.assertTrue(set(sorted(list(panel.index))) == set(sorted(['2317', '2330', '1314'])))
        self.assertTrue(set(sorted(list(panel.columns))) >= set(sorted(['portfolio_value', 'buys', 'date', 'bufwin'])))
        panel = panel.query('buys >=0 and sells >=0 and portfolio_value >=0')  
        self.assertFalse(panel.empty)
        # trans index as map key
        #panel.T.to_dict()

    def test_on_detail(self):
        alg = TwseDualemaAlg(**copy.deepcopy(self._kwargs))
        item = alg.run(alg.to_detail)
        self.assertTrue(len(item)>0)
        self.assertTrue(set(sorted(list(item[0].keys()))) >= set(sorted(['date', 'portfolio_value', 'buy', 'open'])))
    
    def test_on_summary(self):
        alg = TwseDualemaAlg(**copy.deepcopy(self._kwargs))
        alg.run(alg.to_summary)
        item = alg.query_summary(watchtime=datetime.utcnow())
        print item


