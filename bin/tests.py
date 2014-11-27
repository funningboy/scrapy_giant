# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included bin task

import timeit
import re
from celery import group
from main.tests import NoSQLTestCase
from bin.tasks import *
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler

class TestAdd(NoSQLTestCase):

    def test_on_run(self):
        self.assertEqual(3, add.delay(1,2).get())


class TestRunScrapyService(NoSQLTestCase):

    def has_pass(self, fpath):
        try:
            f = open(fpath, 'r')
            c = f.read()
            f.close()
            m = re.findall('Traceback ', c)
            return False if m else True
        except:
            return False

class TestTwseId(TestRunScrapyService):

    def test_on_run(self):
        t = timeit.Timer()
        args = ('twseid', 'INFO', './log/twseid.log', True, True)
        run_scrapy_service.delay(*args).get()
        print "scrapy twseid used %.4f(s)" % (t.timeit())
        self.assertTrue(self.has_pass('./log/twseid.log'))

class TestTwseHisTrader(TestRunScrapyService):

    def test_on_run(self):
        ids = TwseIdDBHandler().stock.get_ids(debug=True)
        ids = list(ids)
        t = timeit.Timer()
        args = ('twsehistrader', 'INFO', './log/twsehistrader.log', True, True)
        run_scrapy_service.delay(*args).get()
        print "scrapy twsehistrader used %.4f(s)/%d(u)" % (t.timeit(), len(ids))
        self.assertTrue(self.has_pass('./log/twsehistrader.log'))

class TestTwseHisStock(TestRunScrapyService):

    def test_on_run(self):
        ids = TwseIdDBHandler().stock.get_ids(debug=True)
        ids = list(ids)
        t = timeit.Timer()
        args = ('twsehisstock', 'INFO', './log/twsehisstock.log', True, True)
        run_scrapy_service.delay(*args).get()
        print "scrapy twsehisstock used %.4f(s)/%d(u)" % (t.timeit(), len(ids))
        self.assertTrue(self.has_pass('./log/twsehisstock.log'))

class TestOtcId(TestRunScrapyService):

    def test_on_run(self):
        t = timeit.Timer()
        args = ('otcid', 'INFO', './log/otcid.log', True, True)
        run_scrapy_service.delay(*args).get()
        print "scrapy otcid used %.4f(s)" % (t.timeit())
        self.assertTrue(self.has_pass('./log/otcid.log'))

class TestOtcHisTrader(TestRunScrapyService):

    def test_on_run(self):
        ids = OtcIdDBHandler().stock.get_ids(debug=True)
        ids = list(ids)
        t = timeit.Timer()
        args = ('otchistrader', 'INFO', './log/otchistrader.log', True, True)
        run_scrapy_service.delay(*args).get()
        print "scrapy otchistrader used %.4f(s)/%d(u)" % (t.timeit(), len(ids))
        self.assertTrue(self.has_pass('./log/otchistrader.log'))

class TestOtcHisStock(TestRunScrapyService):

    def test_on_run(self):
        ids = OtcIdDBHandler().stock.get_ids(debug=True)
        ids = list(ids)
        t = timeit.Timer()
        args = ('otchisstock', 'INFO', './log/otchisstock.log', True, True)
        run_scrapy_service.delay(*args).get()
        print "scrapy otchisstock used %.4f(s)/%d(u)" % (t.timeit(), len(ids))
        self.assertTrue(self.has_pass('./log/otchisstock.log'))

class TestThreadService(TestRunScrapyService):

    def test_on_run(self):
        args = [
            ('twseid', 'INFO', './log/twseid.log', True, False),
            ('otcid', 'INFO', './log/otcid.log', True, False)
        ]
        tasks = group([
            run_scrapy_service.subtask(args[0]),
            run_scrapy_service.subtask(args[1])
        ])
        results = tasks.apply_async()
        results.join()
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())

        args = [
            ('twsehistrader', 'INFO', './log/twsehistrader.log', True, True),
            ('twsehisstock', 'INFO', './log/twsehisstock.log', True, True),
            ('otchistrader', 'INFO', './log/otchistrader.log', True, True),
            ('otchisstock', 'INFO', './log/otchisstock.log', True, True)
        ]
        tasks = group([
            run_scrapy_service.subtask(args[0]),
            run_scrapy_service.subtask(args[1]),
            run_scrapy_service.subtask(args[2]),
            run_scrapy_service.subtask(args[3])
        ])
        t = timeit.Timer()
        results = tasks.apply_async()
        results.join()
        print "scrapy all bin.tasks used %.4f(s)" % (t.timeit())
        self.assertTrue(results.ready())
        self.assertTrue(results.successful())
