# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

#from celery import chain, group
import dill 
import pickle
import timeit
import unittest
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from handler.tasks import *
from bson import json_util
import json

# scrapy crawl twseid -s LOG_FILE=twseid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG
# scrapy crawl traderid -s LOG_FILE=traderid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG
# scrapy crawl twsehistrader2 -s LOG_FILE=twsehistrader2.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG
# scrapy crawl twsehisstock -s LOG_FILE=twsehisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG
# scrapy crawl twsehiscredit -s LOG_FILE=twsehiscredit.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG
# scrapy crawl twsehisfuture -s LOG_FILE=twsehisfuture.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG

skip_tests = {
    'TestTwseHisItemQuery': False,
    'TestTwseHisFrameQuery': False,
    'TestOtcHisItemQuery': False,
    'TestOtcHisFrameQuery': False
}

@unittest.skipIf(skip_tests['TestTwseHisItemQuery'], "skip")
class TestTwseHisItemQuery(NoSQLTestCase):

    def test_on_stock(self):
        stream = pickle.dumps(((), {
            'opt': 'twse',
            'targets': ['stock'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330'],
            'base': 'stock',
            'constraint': lambda x: x.value['eclose'] > 0 and x.value['evolume'] > 0,
            'order': lambda x: [-x.value['totalvolume'], -x.value['eclose']],
            'callback': None,
            'limit': 1,
            'debug': True
        }))
        item = pickle.loads(collect_hisitem.delay(stream).get())
        self.assertTrue(item)
        self.assertTrue(item['stockitem'])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)

    def test_on_trader(self):
        stream = pickle.dumps(((), {
            'opt': 'twse',
            'targets': ['trader'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330'],
            'base': 'stock',
            'constraint': lambda x: x.value['ebuyratio'] > 0 or x.value['totalbuyratio'] > 0,
            'order': lambda x: [-x.value['totalvolume'], -x.value['totalbuyratio']],
            'callback': None,
            'limit': 1,
            'debug': True
        }))
        item = pickle.loads(collect_hisitem.delay(stream).get())
        self.assertTrue(item)
        self.assertTrue(item['traderitem'])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)

    def test_on_credit(self):
        stream = pickle.dumps(((), {
            'opt': 'twse',
            'targets': ['credit'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330'],
            'base': 'stock',
            'constraint': lambda x: x.value['efinanceremain'] > 0 or x.value['ebearfinaratio'] > 0,
            'order': lambda x: [-x.value['ebearfinaratio'], -x.value['totalfinanceremain']],
            'callback': None,
            'limit': 1,
            'debug': True
        }))
        item = pickle.loads(collect_hisitem.delay(stream).get())
        self.assertTrue(item)
        self.assertTrue(item['credititem'])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
 
    def test_on_future(self):
        stream = pickle.dumps(((), {
            'opt': 'twse',
            'targets': ['future'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330'],
            'base': 'stock',
            'constraint': lambda x: x.value['edfcdiff'] > 0 or x.value['totalvolume'] > 0,
            'order': lambda x: [-x.value['edfcdiff'], -x.value['totalvolume']],
            'callback': None,
            'limit': 1,
            'debug': True
        }))
        item = pickle.loads(collect_hisitem.delay(stream).get())
        self.assertTrue(item)
        self.assertTrue(item['futureitem'])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)   

    def test_on_all(self):
        stream = pickle.dumps(((), {
            'opt': 'twse',
            'targets': ['stock', 'trader', 'future', 'credit'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['2317', '2330'],
            'traderids': [],
            'base': 'stock',
            'constraint': None,
            'order': None,
            'callback': None,
            'limit': 2,
            'debug': True
        }))
        item = pickle.loads(collect_hisitem.delay(stream).get())
        self.assertTrue(item)
        [self.assertTrue(item[i]) for i in ['stockitem', 'traderitem', 'credititem', 'futureitem']] 
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)

    def test_on_allid(self):
        stream = pickle.dumps(((), {
            'opt': 'twse',
            'targets': ['stock', 'trader'],
            'callback': None,
            'debug': True
        }))
        item = pickle.loads(collect_iditem.delay(stream).get())
        self.assertTrue(item)
        [self.assertTrue(item[i]) for i in ['stockitem', 'traderitem']]
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)


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
            'constraint': None,
            'order': None,
            'callback': None,
            'limit': 1,
            'debug': True
        }
        panel, _ = collect_hisframe(**kwargs)
        self.assertTrue(panel is not None)
        self.assertFalse(panel.empty)
        self.assertFalse(panel['2317'].empty)
        for k in ['open', 'high', 'low', 'close', 'volume', 'financeremain', 'bearishremain']:
            self.assertFalse(panel['2317'][k].empty)
            self.assertTrue(panel['2317'][k].sum >= 0)
        print panel['2317']


@unittest.skipIf(skip_tests['TestOtcHisItemQuery'], "skip")
class TestOtcHisItemQuery(NoSQLTestCase):

    def test_on_stock(self):
        stream = pickle.dumps(((), {
            'opt': 'otc',
            'targets': ['stock'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['5371', '1565'],
            'base': 'stock',
            'constraint': lambda x: x.value['eclose'] > 0 and x.value['evolume'] > 0,
            'order': lambda x: [-x.value['totalvolume'], -x.value['eclose']],
            'callback': None,
            'limit': 1,
            'debug': True
        }))
        item = pickle.loads(collect_hisitem.delay(stream).get())
        self.assertTrue(item)
        self.assertTrue(item['stockitem'])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)

    def test_on_trader(self):
        stream = pickle.dumps(((), {
            'opt': 'otc',
            'targets': ['trader'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['5371', '1565'],
            'base': 'stock',
            'constraint': lambda x: x.value['ebuyratio'] > 0 or x.value['totalbuyratio'] > 0,
            'order': lambda x: [-x.value['totalvolume'], -x.value['totalbuyratio']],
            'callback': None,
            'limit': 1,
            'debug': True
        }))
        item = pickle.loads(collect_hisitem.delay(stream).get())
        self.assertTrue(item)
        self.assertTrue(item['traderitem'])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)

    def test_on_credit(self):
        stream = pickle.dumps(((), {
            'opt': 'otc',
            'targets': ['credit'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['5371', '1565'],
            'base': 'stock',
            'constraint': lambda x: x.value['efinanceremain'] > 0 or x.value['ebearfinaratio'] > 0,
            'order': lambda x: [-x.value['ebearfinaratio'], -x.value['totalfinanceremain']],
            'callback': None,
            'limit': 1,
            'debug': True
        }))
        item = pickle.loads(collect_hisitem.delay(stream).get())
        self.assertTrue(item)
        self.assertTrue(item['credititem'])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
    
    def test_on_future(self):
        stream = pickle.dumps(((), {
            'opt': 'otc',
            'targets': ['future'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['5371', '1565'],
            'base': 'stock',
            'constraint': lambda x: x.value['edfcdiff'] > 0 or x.value['totalvolume'] > 0,
            'order': lambda x: [-x.value['edfcdiff'], -x.value['totalvolume']],
            'limit': 1,
            'debug': True
        }))
        item = pickle.loads(collect_hisitem.delay(stream).get())
        self.assertTrue(item)
        self.assertTrue(item['futureitem'])
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
    
    def test_on_all(self):
        stream = pickle.dumps(((), {
            'opt': 'otc',
            'targets': ['stock', 'trader', 'future', 'credit'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['5371', '1565'],
            'traderids': [],
            'base': 'stock',
            'constraint': None,
            'order': None,
            'callback': None,
            'limit': 2,
            'debug': True
        }))
        item = pickle.loads(collect_hisitem.delay(stream).get())
        self.assertTrue(item)
        [self.assertTrue(item[i]) for i in ['stockitem', 'traderitem', 'credititem', 'futureitem']] 
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)

    def test_on_allid(self):
        stream = pickle.dumps(((), {
            'opt': 'otc',
            'targets': ['stock', 'trader'],
            'callback': None,
            'debug': True
        }))
        item = pickle.loads(collect_iditem.delay(stream).get())
        self.assertTrue(item)
        [self.assertTrue(item[i]) for i in ['stockitem', 'traderitem']]
        print json.dumps(dict(item), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)


@unittest.skipIf(skip_tests['TestTwseHisFrameQuery'], "skip")
class TestTwseHisFrameQuery(NoSQLTestCase):

    def test_on_all(self):
        kwargs = {
            'opt': 'otc',
            'targets': ['stock', 'trader', 'future', 'credit'],
            'starttime': datetime.utcnow() - timedelta(days=5),
            'endtime': datetime.utcnow(),
            'stockids': ['5371'],
            'traderids': [],
            'base': 'stock',
            'constraint': None,
            'order': None,
            'callback': None,
            'limit': 1,
            'debug': True
        }
        panel, _ = collect_hisframe(**kwargs)
        self.assertTrue(panel is not None)
        self.assertFalse(panel.empty)
        self.assertFalse(panel['5371'].empty)
        for k in ['open', 'high', 'low', 'close', 'volume', 'financeremain', 'bearishremain']:
            self.assertFalse(panel['5371'][k].empty)
            self.assertTrue(panel['5371'][k].sum >= 0)
        print panel['5371']