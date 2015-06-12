# -*- coding: utf-8 -*-

from mongoengine import *

ALG_CHOICES = (
    # map as hisstock_detail/list
    (0, 'StockProfileUp0'),
    (1, 'StockProfileDown0'),
    (2, 'StockProfileUp1'),
    (3, 'StockProfileDown1'),
    # map as histrader_detail/list,
    (4, 'TraderProfileUp0'),
    (5, 'TraderProfileDown0')
    # map as alg
)

OPT_CHOICES = (
    (0, 'twse'),
    (1, 'otc')
)

WIN_CHOICES = (
    (0, '5'),
)


PFL_CHOICES = (
    (0, 'Dualema'),
)

class SearchItem(Document):
    starttime = StringField(required=True, max_length=10, help_text='starttime:2015/01/01')
    endtime = StringField(required=True, max_length=10, help_text='endtime:2015/01/30')
    stockids = StringField(max_length=40, help_text='stockids:2330,2317')
    traderids = StringField(max_length=40, help_text='traderids:1440,1470')
    opt = StringField(required=True, max_length=5, choices=OPT_CHOICES, help_text='opt:twse|otc')
    algorithm = StringField(required=True, max_length=70, choices=ALG_CHOICES, help_text='algorithm')

class PortfolioItem(Document):
    watchtime = StringField(required=True, max_length=10, help_text='watchtime:2015/01/30')
    opt = StringField(required=True, max_length=5, choices=OPT_CHOICES, help_text='opt:twse|otc')
    bufwin = StringField(required=True, max_length=5, choices=WIN_CHOICES, help_text='bufwin:5|10|20|40|80')
    algorithm = StringField(required=True, max_length=70, choices=PFL_CHOICES, help_text='algorithm')
