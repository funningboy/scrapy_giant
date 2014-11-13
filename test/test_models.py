# -*- coding: utf-8 -*-

import unittest
import os
from bson import json_util
import json
import time
import subprocess
import signal
from datetime import datetime

from mongoengine import *
from bin.mongodb_driver import *
from query.models import TraderData, TraderInfo, StockData, TwseHisColl, TwseIdColl, OtcHisColl, OtcIdColl, switch
from test.test_start import *

import django
from django.template import Context, Template
from django.conf import settings

settings.configure(
        USE_TZ=True,
        INSTALLED_APPS=('django.contrib.auth', 'mongoengine.django.mongo_auth'),
        AUTH_USER_MODEL=('mongo_auth.MongoUser'),
        AUTHENTICATION_BACKENDS = ('mongoengine.django.auth.MongoEngineBackend',)
)


class TestTwseIdColl(TestBase):

    def setUp(self):
        super(TestTwseIdColl, self).setUp()
        global TwseIdColl
        connect('twseiddb', host=MongoDBDriver._host, port=MongoDBDriver._port, alias='twseiddb')
        TwseIdColl = switch(TwseIdColl, 'twseiddb')
        TwseIdColl.drop_collection()
        TwseIdColl.ensure_index([('stockid', 1), ('stocknm', 1)])

    def test_on_run(self):
        TwseIdColl(stockid='2317', stocknm=u'紅海').save()
        TwseIdColl(stockid='2330', stocknm=u'台積電').save()
        cursor = TwseIdColl._collection.find({'stockid': '2317'}).limit(1)
        # update as latest
        bulk = TwseIdColl._collection.initialize_ordered_bulk_op()
        bulk.find({'stockid': '2317'}).update({'$set': {'stocknm': u'鴻海'}})
        bulk.execute()
        # iter query
        t = Template("{% for it in item %}{{ it.stockid }}-{{ it.stocknm }}:{% endfor %}")
        d = {"item": TwseIdColl.objects.order_by('stockid')}
        self.assertEqual(t.render(Context(d)), u'2317-鴻海:2330-台積電:')
        cursor = TwseIdColl._coll.find({'stockid': stockid})
        t = Template("{% for it in item %}{{ it.stockid }}-{{ it.stocknm }}:{% endfor %}")
        d = {"item": cursor}
        print t.render(Context(t))

    def tearDown(self):
        super(TestTwseIdColl, self).tearDown()


class TestTwseHisColl(TestBase):

    def setUp(self):
        super(TestTwseHisColl, self).setUp()
        global TraderData, TraderInfo, StockData, TwseHisColl
        connect('twsehisdb', alias='twsehisdb')
        TwseHisColl = switch(TwseHisColl, 'twsehisdb')
        TwseHisColl.drop_collection()
        TwseHisColl.ensure_index([('date', -1), ('stockid', 1), ('stocknm', 1)])

    def test_on_run(self):
        tdata = TraderData(avgbuyprice=10, buyvolume=100, avgsellprice=11, sellvolume=111)
        tinfo = TraderInfo(traderid='1234', tradernm='test', data=tdata)
        sdata = StockData(open=100, high=111, low=99, close=99, volume=1000)
        # iter
        for i in range(2):
            cursor = TwseHisColl.objects(Q(date=datetime.utcnow()) & (Q(stockid='2317') | Q(stocknm=u'鴻海')))
            if cursor.count() == 0:
                coll = TwseHisColl(date=datetime.utcnow()).save()
            else:
                coll = cursor[0]
            coll.stockid='2317'
            coll.stocknm=u'鴻海'
            coll.data=sdata
            coll.topbuylist = [tinfo]
            coll.save()
        # query
        cursor = TwseHisColl.objects.order_by('-stockid')
        for it in cursor:
            t = Template("{% for it in item %}{{ it.traderid }}-{{ it.data.avgbuyprice }}-{{ o.data.buyvitemume }}:{% endfor %}")
            d = {"item": it.topbuylist}
            self.assertEqual(t.render(Context(d)), u'1234-10.0-100:')
        self.assertEqual(len(TwseHisColl.objects), 1)

    def tearDown(self):
        super(TestTwseHisColl, self).tearDown()


if __name__ == '__main__':
    unittest.main()
