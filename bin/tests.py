# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included bin task

import timeit
import unittest
import re
from celery import group
from main.tests import NoSQLTestCase
from bin.tasks import *
from bin.start import wap_scrapy_cmd

# scrapy tests
scrapy_tests = {
    # id table [0:3]
    'twseid': ('twseid', 'INFO', './log/twseid.log', True, False),
    'otcid': ('otcid', 'INFO', './log/otcid.log', True, False),
    'tradeerid': ('traderid', 'INFO', './log/traderid.log', True, False),
    # twsehisdb table [3:8]
    'twsehistrader': ('twsehistrader', 'INFO', './log/twsehistrader.log', True, True),
    'twsehistrader2': ('twsehistrader2', 'INFO', './log/twsehistrader2.log', True, True),
    'twsehisstock': ('twsehisstock', 'INFO', './log/twsehisstock.log', True, True),
    'twsehiscredit': ('twsehiscredit', 'INFO', './log/twsehiscredit.log', True, True),
    'twsehisnocredit': ('twsehisnocredit', 'INFO', './log/twsehisnocredit.log', True, True),
    'twsehisnews': ('twsehisnews', 'INFO', './log/twsehisnews.log', True, True),
    # otchisdb table [8:13]
    'otchistrader': ('otchistrader', 'INFO', './log/otchistrader.log', True, True),
    'otchistrader2': ('otchistrader2', 'INFO', './log/otchistrader2.log', True, True),
    'otchisstock': ('otchisstock', 'INFO', './log/otchisstock.log', True, True),
    'otchiscredit': ('otchiscredit', 'INFO', './log/otchiscredit.log', True, True),
    'otchisnocredit': ('otchisnocredit', 'INFO', './log/otchisnocredit.log', True, True),
    'otchisnews': ('otchisnews', 'INFO', './log/otchisnews.log', True, True)
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
}

@unittest.skipIf(True, 'skip TestAdd')
class TestAdd(NoSQLTestCase):

    def test_on_run(self):
        self.assertEqual(3, add.delay(1,2).get())


class TestRunScrapyService(NoSQLTestCase):

    def setUp(self):
        """ make sure mongodb has start """
        self.assertTrue(has_service())

    def has_pass(self, fpath):
        try:
            f = open(fpath, 'r')
            c = f.read()
            f.close()
            m = re.findall('Traceback|fail ', c)
            return False if m else True
        except:
            return False

    def tearDown(self):
        pass

class TestThreadService(TestRunScrapyService):

    def test_on_run(self):
        # id
        jobs = ['twseid', 'otcid', 'traderid']
        tasks = group([
            run_scrapy_service.subtask(scrapy_tests[k]) for k in jobs
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
        [self.assertTrue(self.has_pass(scrapy_tests[k][2])) for k in jobs]

        # twse
        jobs = ['twsehisstock', 'twsehistrader', 'twsehistrader2', 'twsehiscredit']
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

        # otc
        jobs = ['otchisstock', 'otchistrader', 'otchistradeer2', 'otchiscredit']
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
        self._id = TwseIdDBHandler(**scrapy_kwargs['traderid'])
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
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

class TestTwseId():
    pass

class TestOtcId():
    pass

class TestTwseHisStock():
    pass

class TwstTwseHisTrader():
    pass

