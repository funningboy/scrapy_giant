# -*- coding: utf-8 -*-

from datetime import datetime

from mongoengine import *


class AlgSummaryColl(Document):
    start_time = DateTimeField(default=datetime.utcnow())
    end_time = DateTimeField(default=datetime.utcnow())
    stockid = StringField()
    traderid = StringField()
    portfolio_value = FloatField(min_value=0.0, max_value=999999999.0)
    ending_value = FloatField(min_value=0.0, max_value=999999999.0)
    ending_cash = FloatField(min_value=0.0, max_value=999999999.0)
    capital_used = FloatField(min_value=0.0, max_value=999999999.0)
    buy_count = IntField(min_value=0, max_value=999)
    sell_count = IntField(min_value=0, max_value=999)
    capital_used
    meta = {
        'allow_inheritance': True,
        'indexes': [(
            'stockid', 'traderid', 'start_time', 'end_time', 'portfolio_value',
            'ending_value',  'buy_count', 'sell_count'
        )]
    }


class TwseAlgSummaryColl(AlgSummaryColl):
    pass


class OtcAlgSummaryColl(AlgSummaryColl):
    pass

class AlgDetailData(EmbeddedDocument):
    open = FloatField(min_value=0.0, max_value=9999.0)
    high = FloatField(min_value=0.0, max_value=9999.0)
    low = FloatField(min_value=0.0, max_value=9999.0)
    close = FloatField(min_value=0.0, max_value=9999.0)
    volume = IntField(min_value=0, max_value=9999999)
    ending_value
    ending_cash
    buy = IntField(min_value=0, max_value=1)
    sell = IntField(min_value=0, max_value=1)


class AlgDetailColl(Document):
    meta = {
        'allow_inheritance': True,
    }


class TwseDualemaDetailColl(AlgDetailColl):
    pass


class OtcAlgDetailColl(AlgDetailColl):
    pass

