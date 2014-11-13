# -*- coding: utf-8 -*-

from datetime import datetime

from mongoengine import *
from mongoengine.connection import get_db, get_connection

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

class HisColl(Document):
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

class TwseHisColl(HisColl):
    pass

class OtcHisColl(HisColl):
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


def switch(model, db):
    model._meta['db_alias'] = db
    # must set _collection to none so it is re-evaluated
    model._collection = None
    return model
