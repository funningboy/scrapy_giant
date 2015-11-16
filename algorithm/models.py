# -*- coding: utf-8 -*-

from datetime import datetime
from mongoengine import *

class AlgSummaryColl(EmbeddedDocument):
    stockid = StringField()
    traderid = StringField()
    portfolio_value = FloatField(min_value=-999999999.0, max_value=999999999.0)
    ending_value = FloatField(min_value=-999999999.0, max_value=999999999.0)
    ending_cash = FloatField(min_value=-999999999.0, max_value=999999999.0)
    capital_used = FloatField(min_value=-999999999.0, max_value=999999999.0)
    alpha = FloatField(min_value=-999.0, max_value=999.0)
    beta = FloatField(min_value=-999.0, max_value=999.0)
    sharpe = FloatField(min_value=-999.0, max_value=999.0) 
    max_drawdown = FloatField(min_value=-999.0, max_value=999.0) 
    benchmark_period_return = FloatField(min_value=-999.0, max_value=999.0)
    # 1m, 3m, 6m, 1y pperiod benchmark
    buys = IntField(min_value=0, max_value=999)
    sells = IntField(min_value=0, max_value=999)

    meta = {
        'allow_inheritance': True,
        'indexes': [(
            'portfolio_value', 'capital_used'
            'ending_cash',  'buys', 'sells', 'max_drawdown'
        )],
        'ordering': [('-portfolio_value', '-capital_used', '-max_drawdown')]
    }

class AlgStrategyColl(Document):
    date = DateTimeField(default=datetime.utcnow())
    last_update = DateTimeField()
    cfg = StringField()
    algnm = StringField()
    # ref ptr user
    toplist = ListField(EmbeddedDocumentField(AlgSummaryColl))

    meta = {
        'allow_inheritance': True,
        'indexes': [(
            'date', 'algnm'
        )]
    }

class AlgDetailColl(Document):
    date = DateTimeField(default=datetime.utcnow())
    open = FloatField(min_value=0.0, max_value=9999.0)
    high = FloatField(min_value=0.0, max_value=9999.0)
    low = FloatField(min_value=0.0, max_value=9999.0)
    close = FloatField(min_value=0.0, max_value=9999.0)
    volume = IntField(min_value=0, max_value=9999999)
    portfolio_value = FloatField(min_value=-999999999.0, max_value=999999999.0)
    ending_value = FloatField(min_value=-999999999.0, max_value=999999999.0)
    ending_cash = FloatField(min_value=-999999999.0, max_value=999999999.0)
    capital_used = FloatField(min_value=-999999999.0, max_value=999999999.0)
    buy = IntField(min_value=0, max_value=1)
    sell = IntField(min_value=0, max_value=1)
