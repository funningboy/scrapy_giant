# -*- coding: utf-8 -*-

from mongoengine import *

ALG_CHOICES = (
    # map as hisstock_detail/list
    (0, 'StockProfileUp0'),
    (1, 'StockProfileUp1'),
    (2, 'StockProfileUp2'),
    (3, 'StockProfileDown0'),
    (4, 'StockProfileDown1'),
    (5, 'StockProfileDown2'),
    # map as histrader_detail/list,
    (6, 'TraderProfileUp0'),
    (7, 'TraderProfileUp1'),
    (8, 'TraderProfileDown0'),
    (9, 'TraderProfileDown1')
    # map as alg
)

OPT_CHOICES = (
    (0, 'twse'),
    (1, 'otc')
)

class SearchItem(Document):
    starttime = StringField(required=True, max_length=10, help_text='starttime:2015/01/01')
    endtime = StringField(required=True, max_length=10, help_text='endtime:2015/01/30')
    stockids = StringField(max_length=40, help_text='stockids:2330,2317')
    traderids = StringField(max_length=40, help_text='traderids:1440,1470')
    opt = StringField(required=True, max_length=5, choices=OPT_CHOICES, help_text='opt:twse|otc')
    algorithm = StringField(required=True, max_length=70, choices=ALG_CHOICES, help_text='algorithm')