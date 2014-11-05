# -*- coding: utf-8 -*-

from datetime import datetime

from mongoengine import *
from mongoengine.connection import get_db

#connect(db='tmp')
#self._db = get_db()
#register_connect(host, port, 'tmp')

class TraderData(EmbededDocument):
    avgbuyprice = FloatField(min_value=0, max_value=9999)
    buyvolum = IntField(min_value=0, max_value=9999999)
    avgsellprice = FloatField(min_value=0, max_value=9999)
    sellvolum = IntField(min_value=0, max_value=9999999)

class TraderInfo(EmbededDocument):
    traderid = StringField()
    tradernm = StringField()
    data = EmbeddedDocumentField(TraderData)

class StockData(EmbededDocument):
    open = FloatField(min_value=0, max_value=9999)
    high = FloatField(min_value=0, max_value=9999)
    low = FloatField(min_value=0, max_value=9999)
    close = FloatField(min_value=0, max_value=9999)
    volum = IntField(min_value=0, max_value=9999999)

class HisDB(Document):
    stockid = StringField()
    stocknm = StringField()
    date = DateTimeField(default=datetime.now)
    topselllist = ListField(EmbeddedDocumentField(TraderInfo))
    topbuylist = ListField(EmbeddedDocumentField(TraderInfo))
    data = EmbeddedDocumentField(StockData)

    meta = {
        "allow_inheritance": True,
        'indexes': [('stockid', 'stocknm', '-date')]
    }

class TwseDB(HisDB):
    pass

class OtcDB(HisDB):
    pass

class TopTrader
    traderid
    tradernm
    rank
    list (date, volume ...)

##HisDB as collection name...
#HisDB.drop_collection()
#HisDB.ensure_indexs()
#HisDB._meta['indexes'][0] ...
#self.Person.objects(age__lt=30)
