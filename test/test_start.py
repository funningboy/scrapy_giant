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
from handler.models import TwseHisColl, TwseIdColl, OtcHisColl, OtcIdColl

class TestBase(unittest.TestCase):

    def setUp(self):
        self._proc = start_service() if not has_service() else None

    def tearDown(self):
        if self._proc:
            close_service(self._proc)
        else:
            close_services()


class TestTwseId(TestBase):

    def setUp(self):
        super(TestTwseId, self).setUp()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('twseiddb', host=host, port=port, alias='twseiddb')
        self._idcoll = switch(TwseIdColl, 'twseiddb')
        self._idcoll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl twseid -s LOG_FILE=twseid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._idcoll.objects(Q(stockid='2317')).limit(1)
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTwseId, self).tearDown()


class TestTwseHisTrader(TestBase):

    def setUp(self):
        super(TestTwseHisTrader, self).setUp()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('twsehisdb', host=host, port=port, alias='twsehisdb')
        self._hiscoll = switch(TwseHisColl, 'twsehisdb')
        self._hiscoll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl twsehistrader -s LOG_FILE=twsehistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._hiscoll.objects(Q(stockid='2317')).order_by('-date').limit(1)
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTwseHisTrader, self).tearDown()


class TestTwseHisTrader2(TestBase):

    def setUp(self):
        super(TestTwseHisTrader2, self).setUp()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('twsehisdb', host=host, port=port, alias='twsehisdb')
        self._hiscoll = switch(TwseHisColl, 'twsehisdb')
        self._hiscoll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl twsehistrader2 -s LOG_FILE=twsehistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._hiscoll.objects(Q(stockid='2317')).order_by('-date').limit(1)
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTwseHisTrader2, self).tearDown()


class TestTwseHisStock(TestBase):

    def setUp(self):
        super(TestTwseHisStock, self).setUp()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('twsehisdb', host=host, port=port, alias='twsehisdb')
        self._hiscoll = switch(TwseHisColl, 'twsehisdb')
        self._hiscoll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl twsehisstock -s LOG_FILE=twsehisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._hiscoll.objects(Q(stockid='2317')).order_by('-date').limit(1)
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTwseHisStock, self).tearDown()


class TestTwseHisAll(TestBase):

    def setUp(self):
        super(TestTwseHisAll, self).setUp()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('twsehisdb', host=host, port=port, alias='twsehisdb')
        self._hiscoll = switch(TwseHisColl, 'twsehisdb')
        self._hiscoll.drop_collection()
        # call scrapy
        cmds = [
            'scrapy crawl twseid -s LOG_FILE=twseid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl twsehistrader -s LOG_FILE=twsehistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl twsehistrader2 -s LOG_FILE=twsehistrader2.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl twsehisstock -s LOG_FILE=twsehisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        ]
        for cmd in cmds:
            subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._hiscoll.objects(Q(stockid='2317')).order_by('-date').limit(1)
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestTwseHisAll, self).tearDown()


class TestOtcId(TestBase):

    def setUp(self):
        super(TestOtcId, self).setUp()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('otciddb', host=host, port=port, alias='otciddb')
        self._idcoll = switch(OtcIdColl, 'otciddb')
        self._idcoll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl otcid -s LOG_FILE=otcid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._idcoll.objects(Q(stockid='5371')).limit(1)
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestOtcId, self).tearDown()


class TestOtcHisTrader(TestBase):

    def setUp(self):
        super(TestOtcHisTrader, self).setUp()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('otchisdb', host=host, port=port, alias='otchisdb')
        self._hiscoll = switch(OtcHisColl, 'otchisdb')
        self._hiscoll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl otchistrader -s LOG_FILE=otchistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._hiscoll.objects(Q(stockid='5371')).order_by('-date').limit(1)
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestOtcHisTrader, self).tearDown()


#class TestOtcHisTrader2(TestBase):
#    pass
#
##    def setUp(self):
##        super(TestOtcHisTrader2, self).setUp()
##        host, port = MongoDBDriver._host, MongoDBDriver._port
##        connect('otchisdb', host=host, port=port, alias='otchisdb')
##        self._hiscoll = switch(OtcHisColl, 'otchisdb')
##        self._hiscoll.drop_collection()
##        # call scrapy
##        cmd = 'scrapy crawl otchistrader2 -s LOG_FILE=otchistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
##        subprocess.check_call(cmd, shell=True)
##
##    def test_on_run(self):
##        cursor = self._hiscoll.objects(Q(stockid='5371')).order_by('-date').limit(1)
##        item = list(cursor)[0]
##        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
##        print stream
##
##    def tearDown(self):
##        super(TestOtcHisTrader2, self).tearDown()
##
#
#
class TestOtcHisStock(TestBase):

    def setUp(self):
        super(TestOtcHisStock, self).setUp()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('otchisdb', host=host, port=port, alias='otchisdb')
        self._hiscoll = switch(OtcHisColl, 'otchisdb')
        self._hiscoll.drop_collection()
        # call scrapy
        cmd = 'scrapy crawl otchisstock -s LOG_FILE=otchisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._hiscoll.objects(Q(stockid='5371')).order_by('-date').limit(1)
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestOtcHisStock, self).tearDown()


class TestOtcHisAll(TestBase):

    def setUp(self):
        super(TestOtcHisAll, self).setUp()
        host, port = MongoDBDriver._host, MongoDBDriver._port
        connect('otchisdb', host=host, port=port, alias='otchisdb')
        self._hiscoll = switch(OtcHisColl, 'otchisdb')
        self._hiscoll.drop_collection()
        self._coll = OtcHisColl._collection
        # call scrapy
        cmds = [
            'scrapy crawl otcid -s LOG_FILE=otcid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl otchistrader -s LOG_FILE=otchistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG',
            'scrapy crawl otchisstock -s LOG_FILE=otchisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG'
        ]
        for cmd in cmds:
            subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._hiscoll.objects(Q(stockid='5371')).order_by('-date').limit(1)
        item = list(cursor)[0]
        stream = item.to_json(sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        super(TestOtcHisAll, self).tearDown()


if __name__ == '__main__':
    unittest.main()
