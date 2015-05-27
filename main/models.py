# -*- coding: utf-8 -*-

from mongoengine import *

ALGCHOICES = (

    # map as get_hisstock_detail
    ('0', 'StockProfile_0'),
    ('1', 'StockProfile_1')
    # map as get_histrader_detail,
    ('2', 'TraderProfile_0')
    # map as dualema alg
)

class SearchItem(Document):
    starttime = StringField(required=True, max_length=10, help_text="starttime:2015/01/01")
    endtime = StringField(required=True, max_length=10, help_text="endtime:2015/01/30")
    stockids = StringField(max_length=40, help_text="stockids:2330,2317")
    traderids = StringField(max_length=40, help_text="traderids:1440,1470")
    algorithm = StringField(max_length=70, required=True, choices=ALGCHOICES)
