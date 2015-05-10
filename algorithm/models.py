# -*- coding: utf-8 -*-

from datetime import datetime

from mongoengine import *


class AlgSummaryColl(Document):
    start_time = DateTimeField(default=datetime.utcnow())
    end_time = DateTimeField(default=datetime.utcnow())
    stockid = StringField()
    traderid = StringField()
    portfolio_value = FloatField(min_value=-999999999.0, max_value=999999999.0)
    ending_value = FloatField(min_value=-999999999.0, max_value=999999999.0)
    ending_cash = FloatField(min_value=-999999999.0, max_value=999999999.0)
    capital_used = FloatField(min_value=-999999999.0, max_value=999999999.0)
    buy_count = IntField(min_value=0, max_value=999)
    sell_count = IntField(min_value=0, max_value=999)
    meta = {
        'allow_inheritance': True,
        'indexes': [(
            'end_time', 'portfolio_value',
            'ending_value',  'buy_count', 'sell_count'
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
    }
