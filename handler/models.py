# -*- coding: utf-8 -*-

from datetime import datetime

from mongoengine import *


class TraderData(EmbeddedDocument):
    avgbuyprice = FloatField(min_value=0, max_value=9999)
    buyvolume = IntField(min_value=0, max_value=9999999)
    avgsellprice = FloatField(min_value=0, max_value=9999)
    sellvolume = IntField(min_value=0, max_value=9999999)


class TraderInfo(EmbeddedDocument):
    traderid = StringField()
    tradernm = StringField()
    data = EmbeddedDocumentField(TraderData)


class StockData(EmbeddedDocument):
    open = FloatField(min_value=0, max_value=9999)
    high = FloatField(min_value=0, max_value=9999)
    low = FloatField(min_value=0, max_value=9999)
    close = FloatField(min_value=0, max_value=9999)
    volume = IntField(min_value=0, max_value=9999999)


class StockHisColl(Document):
    stockid = StringField()
    stocknm = StringField()
    date = DateTimeField(default=datetime.utcnow())
    topselllist = ListField(EmbeddedDocumentField(TraderInfo))
    topbuylist = ListField(EmbeddedDocumentField(TraderInfo))
    data = EmbeddedDocumentField(StockData)
    meta = {
        'allow_inheritance': True,
        'indexes': [('stockid', 'stocknm', '-date')]
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
        'allow_inheritance': True,
        'indexes': [('stockid', 'stocknm')]
    }

class TwseIdColl(StockIdColl):
    pass


class OtcIdColl(StockIdColl):
    pass


class TraderIdColl(Document):
    traderid = StringField()
    tradernm = StringField()
    meta = {
        'allow_inheritance': True,
        'indexes': [('traderid', 'tradernm')]
    }

class TraderMapData(EmbeddedDocument):
    volume = IntField(min_value=0, max_value=9999999)
    date = DateTimeField(default=datetime.utcnow())

class TraderMapColl(Document):
    alias = StringField()
    traderid = StringField()
    stockid = StringField()
    base = StringField()
    datalist = ListField(EmbeddedDocumentField(TraderMapData))
    meta = {
        'allow_inheritance': True,
        'indexes': [('stockid', 'traderid', 'alias', 'base')]
    }
