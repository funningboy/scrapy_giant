# -*- coding: utf-8 -*-

from mongoengine import *

ALG_CHOICES = (
    # map as get_hisstock_detail/list
    (0, 'StockProfile0+'),
    (1, 'StockProfile0-'),
    (2, 'StockProfile1+'),
    (3, 'StockProfile1-'),
    # map as get_histrader_detail/list,
    (4, 'TraderProfile0+'),
    (5, 'TraderProfile0-')
    # map as dualema alg
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
    opt = StringField(max_length=5, required=True, choices=OPT_CHOICES, help_text='opt:twse|otc')
    algorithm = StringField(max_length=70, required=True, choices=ALG_CHOICES, help_text='algorithm')

class PortfolioItem(Document):
    pass

