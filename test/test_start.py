# -*- coding: utf-8 -*-

import unittest
import os
from bson import json_util
import json
import time
import subprocess
import signal

from bin.mongodb_driver import *

class TestTwseId(unittest.TestCase):

    def setUp(self):
        if not has_mongodb_service():
            self._proc = start_mongodb_service()
        self._client = connect_mongodb_service()
        # clear db, collection
        self._client.drop_database('twsedb')
        self._db = self._client.tesedb
        self._db.drop_collection('twseidcoll')
        self._coll = self._client.twsedb.twseidcoll
        # call scrapy
        cmd = 'scrapy crawl twseid -s LOG_FILE=twseid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._coll.find({'stockid': '2317'}).limit(1)
        item = list(cursor)[0]
        stream = json.dumps(item, sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        if not has_mongodb_service():
            close_mongodb_service(self._proc)


class TestTwseHisTrader(unittest.TestCase):

    def setUp(self):
        if not has_mongodb_service():
            self._proc = start_mongodb_service()
        self._client = connect_mongodb_service()
        # clear db, collection
        self._client.drop_database('twsedb')
        self._db = self._client.tesedb
        self._db.drop_collection('twsehiscoll')
        self._coll = self._client.twsedb.twsehiscoll
        # call scrapy
        cmd = 'scrapy crawl twsehistrader -s LOG_FILE=twsehistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._coll.find({'stockid': '2317'}).limit(1)
        item = list(cursor)[0]
        stream = json.dumps(item, sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        if not has_mongodb_service():
            close_mongodb_service(self._proc)


class TestTwseHisStock(unittest.TestCase):

    def setUp(self):
        if not has_mongodb_service():
            self._proc = start_mongodb_service()
        self._client = connect_mongodb_service()
        # clear db, collection
        self._client.drop_database('twsedb')
        self._db = self._client.tesedb
        self._db.drop_collection('twsehiscoll')
        self._coll = self._client.twsedb.twsehiscoll
        # call scrapy
        cmd = 'scrapy crawl twsehisstock -s LOG_FILE=twsehisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._coll.find({'stockid': '2317'}).limit(1)
        item = list(cursor)[0]
        stream = json.dumps(item, sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        if not has_mongodb_service():
            close_mongodb_service(self._proc)


class TestTwseHisAll(unittest.TestCase):

    def setUp(self):
        if not has_mongodb_service():
            self._proc = start_mongodb_service()
        self._client = connect_mongodb_service()
        # clear db, collection
        self._client.drop_database('twsedb')
        self._db = self._client.tesedb
        self._db.drop_collection('twsehiscoll')
        self._coll = self._client.twsedb.twsehiscoll
        # call scrapy
        cmds = [
            'scrapy crawl twseid -s LOG_FILE=twseid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1',
            'scrapy crawl twsehistrader -s LOG_FILE=twsehistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1',
            'scrapy crawl twsehisstock -s LOG_FILE=twsehisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1'
        ]
        for cmd in cmds:
            subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._coll.find({'stockid': '2317'}).limit(1)
        item = list(cursor)[0]
        stream = json.dumps(item, sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        if not has_mongodb_service():
            close_mongodb_service(self._proc)


class TestOtcId(unittest.TestCase):

    def setUp(self):
        if not has_mongodb_service():
            self._proc = start_mongodb_service()
        self._client = connect_mongodb_service()
        # clear db, collection
        self._client.drop_database('otcdb')
        self._db = self._client.otcdb
        self._db.drop_collection('otcidcoll')
        self._coll = self._client.otcdb.otcidcoll
        # call scrapy
        cmd = 'scrapy crawl otcid -s LOG_FILE=otcid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._coll.find({'stockid': '5371'}).limit(1)
        item = list(cursor)[0]
        stream = json.dumps(item, sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        if not has_mongodb_service():
            close_mongodb_service(self._proc)


class TestOtcHisTrader(unittest.TestCase):

    def setUp(self):
        if not has_mongodb_service():
            self._proc = start_mongodb_service()
        self._client = connect_mongodb_service()
        # clear db, collletion
        self._client.drop_database('otcdb')
        self._db = self._client.otcdb
        self._db.drop_collection('otchiscoll')
        self._coll = self._db.otchiscoll
        # call scrapy
        cmd = 'scrapy crawl otchistrader -s LOG_FILE=otchistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._coll.find({'stockid': '5371'}).limit(1)
        item = list(cursor)[0]
        stream = json.dumps(item, sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        if not has_mongodb_service():
            close_mongodb_service(self._proc)


class TestOtcHisStock(unittest.TestCase):

    def setUp(self):
        if not has_mongodb_service():
            self._proc = start_mongodb_service()
        self._client = connect_mongodb_service()
        # clear db, collletion
        self._client.drop_database('otcdb')
        self._db = self._client.otcdb
        self._db.drop_collection('otchiscoll')
        self._coll = self._db.otchiscoll
        # call scrapy
        cmd = 'scrapy crawl otchisstock -s LOG_FILE=otchisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1'
        subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._coll.find({'stockid': '5371'}).limit(1)
        item = list(cursor)[0]
        stream = json.dumps(item, sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        if not has_mongodb_service():
            close_mongodb_service(self._proc)


class TestOtcHisAll(unittest.TestCase):

    def setUp(self):
        if not has_mongodb_service():
            self._proc = start_mongodb_service()
        self._client = connect_mongodb_service()
        # clear db, collletion
        self._client.drop_database('otcdb')
        self._db = self._client.otcdb
        self._db.drop_collection('otchiscoll')
        self._coll = self._db.otchiscoll
        # call scrapy
        cmds = [
            'scrapy crawl otcid -s LOG_FILE=otcid.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1',
            'scrapy crawl otchistrader -s LOG_FILE=otchistrader.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1',
            'scrapy crawl otchisstock -s LOG_FILE=otchisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1'
        ]
        for cmd in cmds:
            subprocess.check_call(cmd, shell=True)

    def test_on_run(self):
        cursor = self._coll.find({'stockid': '5371'}).limit(1)
        item = list(cursor)[0]
        stream = json.dumps(item, sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        print stream

    def tearDown(self):
        if not has_mongodb_service():
            close_mongodb_service(self._proc)


if __name__ == '__main__':
    unittest.main()
