# -*- coding: utf-8 -*-

from datetime import datetime

from mongoengine import *

#class AlgorithmSummaryColl(Document):
#    stockid = StringField()
#    stocknm = StringField()
#    date = DateTimeField(default=datetime.utcnow())
#    buy = BooleanField()
#    sell = BooleanField()
#    buy_count = IntField(min_value=0, max_value=99999)
#    sell_count = IntField(min_value=0, max_value=99999)
#    portfolio_value = FloatField(min_value=0, max_value=999999999)
#    ending_value = FloatField(min_value=0, max_value=999999999)
#    ending_cash = FloatField(min_value=0, max_value=999999999)
#    open = FloatField(min_value=0, max_value=9999)
#    high = FloatField(min_value=0, max_value=9999)
#    low = FloatField(min_value=0, max_value=9999)
#    close = FloatField(min_value=0, max_value=9999)
#    volume = IntField(min_value=0, max_value=9999999)
#    meta = {
#        'allow_inheritance': True,
#        'indexes': [('stockid', 'stocknm', 'date')]
#    }
#
#
#class AlgorithmDetailColl(Document):
#    from_date = DateTimeField(default=datetime.utcnow())
#    to_date = DateTimeField()
#    portfolio_value = FloatField(min_value=0, max_value=999999999)
#    starting_cash = FloatField(min_value=0, max_value=999999999)
#    starting_value = FloatField(min_value=0, max_value=999999999)
#    ending_value = FloatField(min_value=0, max_value=999999999)
#    ending_cash = FloatField(min_value=0, max_value=999999999)
#    capital_used = IntField(min_value=0, max_value=9999999)
#    period_close = DateTimeField(default=datetime.utcnow())
#    period_open = DateTimeField(default=datetime.utcnow())
#    meta = {
#        'allow_inheritance': True,
#        'indexes': [('date')]
#    }
