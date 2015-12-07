# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

import dill
import pickle
import unittest
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from algorithm.tasks import *

skip_tests = {
    'TestDualEMADetail': False,
    'TestDualEMASummary': False,
    'TestBestTraderDetail': False,
    'TestBestTraderSummary': False
}

@unittest.skipIf()
class TestBestTraderDetail():

    def test_on_to_detail(self):
        stream = pickle.dumps(((), {
            'opt': 'twse',
            'targets': ['besttrader'],
            #'starttime':
            #'endtime':
        }))

@unittest.skipIf(skip_tests['TestDualEMADetail'], "skip")
class TestDualEMADetail(NoSQLTestCase):

    def test_on_to_detail(self):
        stream = pickle.dumps(((), {
            'opt': 'twse',
            'targets': ['dualema'],
            'starttime': datetime.utcnow() - timedelta(days=150),
            'endtime': datetime.utcnow(),
            'base': 'stock',
            'stockids': ['2330'],
            'reserved': False,
            'constraint': lambda x: x.key['algnm'] == 'dualema' and x.value['buys'] >= 0 and x.value['sells'] >= 0,
            'order': lambda x: [-x.value['portfolio'], -x.value['used']],
            'limit': 1,
            'callback': 'to_detail',
            'debug': True,
            'cfg': {
                'buf_win': 30,
                'short_ema_win': 20,
                'long_ema_win': 40
            }
        }))  
        item = pickle.loads(run_algitem.delay(stream).get())
        self.assertTrue(item)
        self.assertTrue(item['dualemaitem'])  
        self.assertTrue(len(item['dualemaitem'])>0)
        self.assertTrue(set(sorted(list(item['dualemaitem'][0].keys()))) >= set(sorted(['date', 'portfolio_value', 'buy', 'open'])))

@unittest.skipIf(skip_tests['TestDualEMASummary'], "skip")
class TestDualEMASummary(NoSQLTestCase):

    def test_on_to_summary(self):
        stream = pickle.dumps(((), {
            'opt': 'twse',
            'targets': ['dualema'],
            'starttime': datetime.utcnow() - timedelta(days=150),
            'endtime': datetime.utcnow(),
            'base': 'stock',
            'stockids': ['2317', '2330', '1314'],
            'reserved': False,
            'constraint': lambda x: x.key['algnm'] == 'dualema' and x.value['buys'] >=0 and x.value['sells'] >= 0,
            'order': lambda x: [-x.value['portfolio'], -x.value['used']],
            'limit': 3,
            'callback': 'insert_summary',
            'debug': True,
            'cfg': {
                'buf_win': 30,
                'short_ema_win': 20,
                'long_ema_win': 40
            }
        })) 
        alg = AlgRegister.algcls('dualema')
        alg = algdb_tasks['twse'](alg, debug=True) 
        alg.algcoll.drop_collection()
        run_algitem.delay(stream).get()
        # query summary factor back and check
        starttime, endtime = datetime.utcnow() - timedelta(days=5), datetime.utcnow()
        stream = pickle.dumps(((), {
            'opt': 'twse',
            'targets': ['dualema'],
            'starttime': starttime,
            'endtime': endtime,
            'base': 'stock',
            'stockids': ['2317', '2330', '1314'],
            'reserved': False,
            'constraint': lambda x: x.key['algnm'] == 'dualema' and x.value['buys'] >=0 and x.value['sells'] >= 0,
            'order': lambda x: [-x.value['portfolio'], -x.value['used']],
            'limit': 1,
            'debug': True,
            'cfg': {
                'buf_win': 30,
                'short_ema_win': 20,
                'long_ema_win': 40
            }
        })) 
        item = pickle.loads(collect_algitem.delay(stream).get())
        self.assertTrue(item)
        self.assertTrue(item['dualemaitem'])
        self.assertTrue(len(item['dualemaitem'])>0)
        self.assertTrue(set(sorted(list(item['dualemaitem'][0].keys()))) >= set(sorted(['portfolio', 'buys'])))
