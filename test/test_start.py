# -*- coding: utf-8 -*-

import unittest
import os
from bson import json_util
import json
import time
import subprocess
import signal

from mongoengine import *
from bin.mongodb_driver import *
from bin.start import switch
from handler.iddb_handler import *
from handler.hisdb_handler import *

class TestBase(unittest.TestCase):

    def setUp(self):
        self._proc = start_service() if not has_service() else None

    def tearDown(self):
        if self._proc:
            close_service(self._proc)
        else:
            close_services()


class TestTraderId(TestBase):

    def setUp(self):
        super(TestTraderId, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'twse'
        }
        self._id = TwseIdDBHandler(**kwargs)
        self._id.trader.coll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl traderid -s LOG_FILE=treaderid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['1590', '1440', '1470']
        cursor = self._id.trader.coll.objects(Q(traderid__in=expect))
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTraderId, self).tearDown()


class TestTwseId(TestBase):

    def setUp(self):
        super(TestTwseId, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'twse'
        }
        self._id = TwseIdDBHandler(**kwargs)
        self._id.stock.coll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl twseid -s LOG_FILE=twseid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['2317', '1314', '2330']
        cursor = self._id.stock.coll.objects(Q(stockid__in=expect))
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTwseId, self).tearDown()


class TestTwseHisTrader(TestBase):

    def setUp(self):
        super(TestTwseHisTrader, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'twse'
        }
        self._db = TwseHisDBHandler(**kwargs)
        self._db.trader.coll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl twsehistrader -s LOG_FILE=twsehistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['2317', '1314', '2330']
        cursor = self._db.trader.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTwseHisTrader, self).tearDown()


class TestTwseHisTrader2(TestBase):

    def setUp(self):
        super(TestTwseHisTrader2, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'twse'
        }
        self._db = TwseHisDBHandler(**kwargs)
        self._db.trader.coll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl twsehistrader2 -s LOG_FILE=twsehistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['2317', '1314', '2330']
        cursor = self._db.trader.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTwseHisTrader2, self).tearDown()


class TestTwseHisStock(TestBase):

    def setUp(self):
        super(TestTwseHisStock, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'twse'
        }
        self._db = TwseHisDBHandler(**kwargs)
        self._db.stock.coll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl twsehisstock -s LOG_FILE=twsehisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['2317', '1314', '2330']
        cursor = self._db.stock.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTwseHisStock, self).tearDown()


#class TestTwseHisCredit(TestBase):
#
#    def setUp(self):
#        super(TestTwseHisCredit, self).setUp()
#        kwargs = {
#            'debug': True,
#            'opt': 'twse'
#        }
#        self._db = TwseHisDBHandler(**kwargs)
#        self._db.credit.coll.drop_collection()
#        # call scrapy
#        cmd = 'scrapy crawl twsehiscredit -s LOG_FILE=twsehiscredit.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
#        subprocess.check_call(cmd, shell=True)
#
#    def test_on_run(self):
#        expect = ['2317', '1314', '2330']
#        cursor = self._db.credit.coll.objects(Q(stockid__in=expect)).order_by('-date')
#        item = list(cursor)[0]
#        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
#        print stream
#
#    def tearDown(self):
#        super(TestTwseId, self).tearDown()


class TestTwseHisAll(TestBase):

    def setUp(self):
        super(TestTwseHisAll, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'twse'
        }
        self._db = TwseHisDBHandler(**kwargs)
        self._db.stock.coll.drop_collection()
        self._db.trader.coll.drop_collection()
        #self._db.credit.coll.drop_collection()
        # call scrapy
        cmds = [
            'scrapy crawl twseid -s LOG_FILE=twseid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl traderid -s LOG_FILE=traderid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_FILE=DEBUG',
            'scrapy crawl twsehistrader -s LOG_FILE=twsehistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl twsehistrader2 -s LOG_FILE=twsehistrader2.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl twsehisstock -s LOG_FILE=twsehisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            #'scrapy crawl twsehiscredit -s LOG_FILE=twsehiscredit.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        ]
        for cmd in cmds:
            subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['2317', '1314', '2330']
        cursor = self._db.stock.coll.objects(Q(stockid__in=expect)).order_by('-date').limit(1)
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTwseHisAll, self).tearDown()


class TestOtcId(TestBase):

    def setUp(self):
        super(TestOtcId, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'otc'
        }
        self._id = OtcIdDBHandler(**kwargs)
        self._id.stock.coll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl otcid -s LOG_FILE=otcid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['5371', '1565', '3105']
        cursor = self._id.stock.coll.objects(Q(stockid__in=expect))
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestOtcId, self).tearDown()


class TestOtcHisTrader(TestBase):

    def setUp(self):
        super(TestOtcHisTrader, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'otc'
        }
        self._db = OtcHisDBHandler(**kwargs)
        self._db.trader.coll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl otchistrader -s LOG_FILE=otchistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['5371', '1565', '3105']
        cursor = self._db.trader.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestOtcHisTrader, self).tearDown()


class TestOtcHisTrader2(TestBase):

    def setUp(self):
        super(TestOtcHisTrader2, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'otc'
        }
        self._db = OtcHisDBHandler(**kwargs)
        self._db.trader.coll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl otchistrader2 -s LOG_FILE=otchistrader2.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['5371', '1565', '3105']
        cursor = self._db.trader.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestOtcHisTrader2, self).tearDown()


class TestOtcHisStock(TestBase):

    def setUp(self):
        super(TestOtcHisStock, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'otc'
        }
        self._db = OtcHisDBHandler(**kwargs)
        self._db.stock.coll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl otchisstock -s LOG_FILE=otchisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['5371', '1565', '3105']
        cursor = self._db.stock.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestOtcHisStock, self).tearDown()


#class TestOtcHisCredit(TestBase):
#
#    def setUp(self):
#        super(TestOtcHisCredit, self).setUp()
#        kwargs = {
#            'debug': True,
#            'opt': 'otc'
#        }
#        self._db = OtcHisDBHandler(**kwargs)
#        self._db.credit.coll.drop_collection()
#        # call scrapy
#        cmd = 'scrapy crawl otchiscredit -s LOG_FILE=otchiscredit.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
#        subprocess.check_call(cmd, shell=True)
#
#    def test_on_run(self):
#        expect = ['5371', '1565', '3105']
#        cursor = self._db.credit.coll.objects(Q(stockid__in=expect)).order_by('-date')
#        item = list(cursor)[0]
#        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
#        print stream
#
#    def tearDown(self):
#        super(TestOtcHisStock, self).tearDown()


class TestOtcHisAll(TestBase):

    def setUp(self):
        super(TestOtcHisAll, self).setUp()
        kwargs = {
            'debug': True,
            'opt': 'otc'
        }
        self._db = OtcHisDBHandler(**kwargs)
        self._db.stock.coll.drop_collection()
        self._db.trader.coll.drop_collection()
        #self._db.credit.coll.drop_collection()
        # call scrapy
        cmds = [
            'scrapy crawl otcid -s LOG_FILE=otcid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl traderid -s LOG_FILE=traderid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl otchistrader -s LOG_FILE=otchistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl otchistrader2 -s LOG_FILE=otchistrader2.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl otchisstock -s LOG_FILE=otchisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
#            'scrapy crawl otchiscredit -s LOG_FILE=otchiscredit.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_FILE=DEBUG'
        ]
        for cmd in cmds:
            subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        expect = ['5371', '1565', '3105']
        cursor = self._db.stock.coll.objects(Q(stockid__in=expect)).order_by('-date')
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestOtcHisAll, self).tearDown()


if __name__ == '__main__':
    unittest.main()
