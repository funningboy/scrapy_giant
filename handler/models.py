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
    tradernm = StringField()
    data = EmbeddedDocumentField(TraderData)

class StockData(EmbeddedDocument):
    open = FloatField(min_value=0.0, max_value=9999.0)
    high = FloatField(min_value=0.0, max_value=9999.0)
    low = FloatField(min_value=0.0, max_value=9999.0)
    close = FloatField(min_value=0.0, max_value=9999.0)
    volume = IntField(min_value=0, max_value=9999999)
    price = FloatField(min_value=0.0, max_value=9999999.0)

class CreditData(EmbeddedDocument):
    buyvolume = IntField(min_value=0, max_value=9999999)
    sellvolume = IntField(min_value=0, max_value=9999999)
    daytrade = IntField(min_value=0, max_value=9999999)
    limit = IntField(min_value=0, max_value=9999999)

class StockHisColl(Document):
    stockid = StringField()
    stocknm = StringField()
    date = DateTimeField(default=datetime.utcnow())
    toplist = ListField(EmbeddedDocumentField(TraderInfo))
    data = EmbeddedDocumentField(StockData)
    finance = EmbeddedDocumentField(CreditData)
    bearish = EmbeddedDocumentField(CreditData)
    meta = {
        'db_alias': 'stockhisdb',
        'allow_inheritance': True,
        'indexes': [('stockid', 'stocknm', 'date')]
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
        'db_alias': 'traderiddb',
        'allow_inheritance': True,
        'indexes': [('traderid', 'tradernm')]
    }

class StockMapData(EmbeddedDocument):
    open = FloatField(min_value=0.0, max_value=9999.0)
    high = FloatField(min_value=0.0, max_value=9999.0)
    low = FloatField(min_value=0.0, max_value=9999.0)
    close = FloatField(min_value=0, max_value=9999.0)
    volume = IntField(min_value=0, max_value=9999999)
    price = FloatField(min_value=0.0, max_value=9999999.0)
    date = DateTimeField(default=datetime.utcnow())

    @property
    def keys(self):
        #return as order html tags
        return ['date', 'open', 'high', 'low', 'close', 'volume', 'price']

    @property
    def values(self):
        return [self.__dict__['_data'][k] for k in self.keys]

    @property
    def items(self):
        return [(k, self.__dict__['_data'][k]) for k in self.keys]

class StockMapColl(Document):
    url = StringField()
    stockid = StringField()
    stocknm = StringField()
    datalist = ListField(EmbeddedDocumentField(StockMapData))
    meta = {
        'db_alias': 'stockmapdb',
        'allow_inheritance': True,
        'indexes': [('stockid')]
    }

    @property
    def keys(self):
        #return as order html tags
        return ['stockid', 'stocknm', 'datalist']

    @property
    def values(self):
        return [self.__dict__['_data'][k] for k in self.keys]

    @property
    def items(self):
        return [(k, self.__dict__['_data'][k]) for k in self.keys]

class TraderMapData(EmbeddedDocument):
    ratio = FloatField(min_value=0.0, max_value=100.0)
    price = FloatField(min_value=0.0, max_value=9999.0)
    buyvolume = IntField(min_value=0, max_value=9999999)
    sellvolume = IntField(min_value=0, max_value=9999999)
    date = DateTimeField(default=datetime.utcnow())

    @property
    def keys(self):
        # return as order html tags
        return ['date', 'ratio','price', 'buyvolume', 'sellvolume']

    @property
    def values(self):
        return [self.__dict__['_data'][k] for k in self.keys]

    @property
    def items(self):
        return [(k, self.__dict__['_data'][k]) for k in self.keys]

class TraderMapColl(Document):
    url = StringField()
    alias = StringField()
    traderid = StringField()
    tradernm = StringField()
    stockid = StringField()
    stocknm = StringField()
    totalvolume = IntField(min_value=0, max_value=9999999)
    totalhit = IntField(min_value=0, max_value=9999999)
    datalist = ListField(EmbeddedDocumentField(TraderMapData))
    meta = {
        'db_alias': 'tradermapdb',
        'allow_inheritance': True,
        'indexes': [('stockid', 'traderid', 'alias')]
    }

    @property
    def keys(self):
        # return as order html tags
        return ['alias', 'traderid', 'tradernm', 'stockid', 'stocknm', 'totalvolume', 'totalhit', 'datalist']

    @property
    def values(self):
        return [self.__dict__['_data'][k] for k in self.keys]

    @property
    def items(self):
        return [(k, self.__dict__['_data'][k]) for k in self.keys]

class CreditMapColl(Document):
    pass
