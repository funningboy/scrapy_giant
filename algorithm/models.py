# -*- coding: utf-8 -*-

from datetime import datetime
from mongoengine import *

class AlgSummaryColl(Document):
    bufwin = IntField(min_value=5, max_value=150)
    endtime = DateTimeField(default=datetime.utcnow())
    stockid = StringField()
    traderid = StringField()
    portfolio_value = FloatField(min_value=-999999999.0, max_value=999999999.0)
    ending_value = FloatField(min_value=-999999999.0, max_value=999999999.0)
    ending_cash = FloatField(min_value=-999999999.0, max_value=999999999.0)
    capital_used = FloatField(min_value=-999999999.0, max_value=999999999.0)
    buys = IntField(min_value=0, max_value=999)
    sells = IntField(min_value=0, max_value=999)
    meta = {
        'allow_inheritance': True,
        'indexes': [(
            'endtime', 'portfolio_value',
            'ending_value',  'buys', 'sells'
        )]
    }


class AlgDetailColl(Document):
    time = DateTimeField(default=datetime.utcnow())
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
    meta = {
        'allow_inheritance': True,
        'indexes': [(
            'time'
            )]
    }
