# -*- coding: utf-8 -*-

from datetime import datetime

from mongoengine import *

class AlgorithmData(EmbeddedDocument):
    stockid = StringField()
    traderid = StringField()
    portfolio_value = FloatField(min_value=0.0, max_value=999999999.0)
    ending_value = FloatField(min_value=0.0, max_value=999999999.0)
    ending_cash = FloatField(min_value=0.0, max_value=999999999.0)
    buy_count = IntField(min_value=0, max_value=999)
    sell_count = IntField(min_value=0, max_value=999)
    meta = {
        'indexes': [(
            'stockid', 'traderid', 'date', 'algnm', 'portfolio_value',
            'ending_value',  'buy_count', 'sell_count'
        )]
    }

class AlgorithmColl(Document):
    algnm = StringField()
    date = DateTimeField(default=datetime.utcnow())
    datalist = ListField(EmbeddedDocument(AlgorithmData))
    meta = {
        'db_alias': 'algdb',
        'allow_inheritance': True,
        'indexes': [('algnm', 'date')]
    }
