# -*- coding: utf-8 -*-

from datetime import datetime
from mongoengine import *

class TraderData(EmbeddedDocument):
    avgbuyprice = FloatField(min_value=0.0, max_value=9999.0)
    buyvolume = IntField(min_value=0, max_value=9999999)
    avgsellprice = FloatField(min_value=0.0, max_value=9999.0)
    sellvolume = IntField(min_value=0, max_value=9999999)
    totalvolume = IntField(min_value=0, max_value=9999999)

class TraderInfo(EmbeddedDocument):
    traderid = StringField()
    data = EmbeddedDocumentField(TraderData)

class StockData(EmbeddedDocument):
    open = FloatField(min_value=0.0, max_value=9999.0)
    high = FloatField(min_value=0.0, max_value=9999.0)
    low = FloatField(min_value=0.0, max_value=9999.0)
    close = FloatField(min_value=0.0, max_value=9999.0)
    volume = IntField(min_value=0, max_value=9999999)
    price = FloatField(min_value=0.0, max_value=9999999.0)

class CreditData(EmbeddedDocument):
    preremain = IntField(min_value=0, max_value=9999999)
    curremain = IntField(min_value=0, max_value=9999999)
    buyvolume = IntField(min_value=0, max_value=9999999)
    sellvolume = IntField(min_value=0, max_value=9999999)
    daytrade = IntField(min_value=0, max_value=9999999)
    limit = IntField(min_value=0, max_value=9999999)

class StockHisColl(Document):
    stockid = StringField()
    date = DateTimeField(default=datetime.utcnow())
    toplist = ListField(EmbeddedDocumentField(TraderInfo))
    data = EmbeddedDocumentField(StockData)
    finance = EmbeddedDocumentField(CreditData)
    bearish = EmbeddedDocumentField(CreditData)
    #future
    #event
    meta = {
        'db_alias': 'stockhisdb',
        'allow_inheritance': True,
        'indexes': [('stockid', 'date')],
        'ordering': [('-date')]
    }

class TwseHisColl(StockHisColl):
    pass

class OtcHisColl(StockHisColl):
    pass

class StockIdColl(Document):
    stockid = StringField()
    stocknm = StringField()
    industry = StringField()
    onmarket = StringField()
    meta = {
        'db_alias': 'stockiddb',
        'allow_inheritance': True,
        'indexes': [('stockid', 'stocknm')],
        'ordering': [('+stockid')]
    }

class TwseIdColl(StockIdColl):
    pass


class OtcIdColl(StockIdColl):
    pass


class TraderIdColl(Document):
    traderid = StringField()
    tradernm = StringField()
    meta = {
        'db_alias': 'traderiddb',
        'allow_inheritance': True,
        'indexes': [('traderid', 'tradernm')],
        'ordering': [('+traderid')]
    }