# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included bin task

# start rabbitmq, mongodb, celery
import timeit
import unittest
from mongoengine import *
import re
import time
from celery import group
from main.tests import NoSQLTestCase
from bin.tasks import *
from handler.tasks import iddb_tasks, hisdb_tasks
from bin.start import wap_scrapy_cmd
from bson import json_util
import json

# scrapy tests
scrapy_tests = {
    # id table [0:3]
    'twseid': ('twseid', 'DEBUG', './log/test_twseid.log', True, True),
    'otcid': ('otcid', 'DEBUG', './log/test_otcid.log', True, True),
    'traderid': ('traderid', 'DEBUG', './log/test_traderid.log', True, True),
    # twsehisdb table [3:8]
    'twsehistrader': ('twsehistrader', 'DEBUG', './log/test_twsehistrader.log', True, True),
    'twsehistrader2': ('twsehistrader2', 'DEBUG', './log/test_twsehistrader2.log', True, True),
    'twsehisstock': ('twsehisstock', 'DEBUG', './log/test_twsehisstock.log', True, True),
    'twsehiscredit': ('twsehiscredit', 'DEBUG', './log/test_twsehiscredit.log', True, True),
    'twsehisnocredit': ('twsehisnocredit', 'DEBUG', './log/test_twsehisnocredit.log', True, True),
    'twsehisnews': ('twsehisnews', 'DEBUG', './log/test_twsehisnews.log', True, True),
    'twsehisfuture': ('twsehisfuture', 'DEBUG', './log/test_twsehisfuture.log', True, True),
    # otchisdb table [8:13]
    'otchistrader': ('otchistrader', 'DEBUG', './log/test_otchistrader.log', True, True),
    'otchistrader2': ('otchistrader2', 'DEBUG', './log/test_otchistrader2.log', True, True),
    'otchisstock': ('otchisstock', 'DEBUG', './log/test_otchisstock.log', True, True),
    'otchiscredit': ('otchiscredit', 'DEBUG', './log/test_otchiscredit.log', True, True),
    'otchisnocredit': ('otchisnocredit', 'DEBUG', './log/test_otchisnocredit.log', True, True),
    'otchisnews': ('otchisnews', 'DEBUG', './log/test_otchisnews.log', True, True),
    'otchisfuture': ('otchisfuture', 'DEBUG', './log/test_otchisfuture.log', True, True)
}

# scrapy kwargs
scrapy_kwargs = {
    'twseid': {
        'debug': True,
        'opt': 'twse'
    },
    'otcid' : {
        'debug': True,
        'opt': 'otc'
    },
    'traderid': {
        'debug': True,
        'opt': 'twse'
    },
    'twsehisstock': {
        'debug': True,
        'opt': 'twse'
    },
    'twsehistrader': {
        'debug': True,
        'opt': 'twse'
    },
    'twsehistrader2': {
        'debug': True,
        'opt': 'twse'
    },
    'twsehistrader2': {
        'debug': True,
        'opt': 'twse'
    },
    'twsehiscredit': {
        'debug': True,
        'opt': 'twse'
    },
    'twsehisfuture': {
        'debug': True,
        'opt': 'twse'
    },
    'otchisstock': {
        'debug': True,
        'opt': 'otc'
    },
    'otchistrader': {
        'debug': True,
        'opt': 'otc'
    },
    'otchistrader2': {
        'debug': True,
        'opt': 'otc'
    },
    'otchistrader2': {
        'debug': True,
        'opt': 'otc'
    },
    'otchiscredit': {
        'debug': True,
        'opt': 'otc'
    },
    'otchisfuture': {
        'debug': True,
        'opt': 'otc'
    }
}

@unittest.skipIf(True, 'skip TestAdd')
class TestAdd(NoSQLTestCase):

    def test_on_run(self):
        self.assertEqual(3, add.delay(1,2).get())


class TestRunScrapyService(NoSQLTestCase):

    def setUp(self):
        pass

    def has_pass(self, fpath):
        try:
            f = open(fpath, 'r')
            c = f.read()
            f.close()
            m = re.findall('exceptions\.', c)
            return False if m else True
        except:
            return False

    def tearDown(self):
        pass

class TestTwseThreadService(TestRunScrapyService):

    def test_on_run(self):
        # id
        jobs = ['twseid', 'traderid']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        [self.assertTrue(self.has_pass(scrapy_tests[k][2])) for k in jobs]

        # twse
        jobs = ['twsehisstock', 'twsehistrader2', 'twsehiscredit', 'twsehisfuture']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        t = timeit.Timer()
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        [self.assertTrue(self.has_pass(scrapy_tests[k][2])) for k in jobs]
        print "scrapy twsehisdb bin.tasks used %.4f(s)" % (t.timeit())

class TestOtcThreadService(TestRunScrapyService):

    def test_on_run(self):
        # id
        jobs = ['otcid', 'traderid']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        [self.assertTrue(self.has_pass(scrapy_tests[k][2])) for k in jobs]

        # otc
        jobs = ['otchisstock', 'otchistrader2', 'otchiscredit', 'otchisfuture']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        t = timeit.Timer()
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        [self.assertTrue(self.has_pass(scrapy_tests[k][2])) for k in jobs]
        print "scrapy otchisdb bin.tasks used %.4f(s)" % (t.timeit())

class TestTraderId(TestRunScrapyService):

    def test_on_run(self):
        self._id = iddb_tasks['twse'](**scrapy_kwargs['traderid'])
        self._id.trader.coll.drop_collection()
        jobs = ['traderid']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = self._id.trader.get_ids()
        cursor = self._id.trader.coll.objects(Q(traderid__in=expect))
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

class TestTwseId(TestRunScrapyService):
    
    def test_on_run(self):
        self._id = iddb_tasks['twse'](**scrapy_kwargs['twseid'])
        self._id.stock.coll.drop_collection()
        jobs = ['twseid']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = self._id.stock.get_ids()
        expect = ['2330']
        cursor = self._id.stock.coll.objects(Q(stockid__in=expect))
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

class TestOtcId(TestRunScrapyService):

    def test_on_run(self):
        self._id = iddb_tasks['otc'](**scrapy_kwargs['otcid'])
        self._id.stock.coll.drop_collection()
        jobs = ['otcid']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = self._id.stock.get_ids()
        expect = ['5371']
        cursor = self._id.stock.coll.objects(Q(stockid__in=expect))
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

class TestTwseHisStock(TestRunScrapyService):
  
    def test_on_run(self):
        self._db = hisdb_tasks['twse'](**scrapy_kwargs['twsehisstock'])
        self._db.stock.coll.drop_collection()
        jobs = ['twsehisstock']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = ['2317', '1314', '2330']
        cursor = self._db.stock.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

@unittest.skipIf(True, 'skip')
class TestTwseHisTrader(TestRunScrapyService):

    def test_on_run(self):
        self._db = hisdb_tasks['twse'](**scrapy_kwargs['twsehistrader'])
        self._db.trader.coll.drop_collection()
        jobs = ['twsehistrader']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = ['2317', '1314', '2330']
        cursor = self._db.trader.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

class TestTwseHisTrader2(TestRunScrapyService):

    def test_on_run(self):
        self._db = hisdb_tasks['twse'](**scrapy_kwargs['twsehistrader2'])
        self._db.trader.coll.drop_collection()
        jobs = ['twsehistrader2']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = ['2317', '1314', '2330']
        cursor = self._db.trader.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

class TestTwseHisCredit(TestRunScrapyService):

    def test_on_run(self):
        self._db = hisdb_tasks['twse'](**scrapy_kwargs['twsehiscredit'])
        self._db.credit.coll.drop_collection()
        jobs = ['twsehiscredit']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = ['2317', '1314', '2330']
        cursor = self._db.credit.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream
    
class TestTwseHisFuture(TestRunScrapyService):
    
    def test_on_run(self):
        self._db = hisdb_tasks['twse'](**scrapy_kwargs['twsehisfuture'])
        self._db.future.coll.drop_collection()
        jobs = ['twsehisfuture']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = ['2317', '1314', '2330']
        cursor = self._db.future.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

class TestOtcHisStock(TestRunScrapyService):
    
    def test_on_run(self):
        self._db = hisdb_tasks['otc'](**scrapy_kwargs['otchisstock'])
        self._db.stock.coll.drop_collection()
        jobs = ['otchisstock']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = ['5371', '1565', '3105']
        cursor = self._db.stock.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

@unittest.skipIf(True, 'skip')
class TestOtcHisTrader(TestRunScrapyService):
    
    def test_on_run(self):
        self._db = hisdb_tasks['otc'](**scrapy_kwargs['otchistrader'])
        self._db.trader.coll.drop_collection()
        jobs = ['otchistrader']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = ['5371', '1565', '3105']
        cursor = self._db.trader.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

class TestOtcHisTrader2(TestRunScrapyService):
    
    def test_on_run(self):
        self._db = hisdb_tasks['otc'](**scrapy_kwargs['otchistrader2'])
        self._db.trader.coll.drop_collection()
        jobs = ['otchistrader2']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = ['5371', '1565', '3105']
        cursor = self._db.trader.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

class TestOtcHisCredit(TestRunScrapyService):
    
    def test_on_run(self):
        self._db = hisdb_tasks['otc'](**scrapy_kwargs['otchiscredit'])
        self._db.credit.coll.drop_collection()
        jobs = ['otchiscredit']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = ['5371', '1565', '3105']
        cursor = self._db.credit.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream
    
class TestOtcHisFuture(TestRunScrapyService):
    
    def test_on_run(self):
        self._db = hisdb_tasks['otc'](**scrapy_kwargs['otchisfuture'])
        self._db.future.coll.drop_collection()
        jobs = ['otchisfuture']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        expect = ['5371', '1565', '3105']
        cursor = self._db.future.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        print stream

