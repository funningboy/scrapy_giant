# -*- coding: utf-8 -*-

from mongoengine import *
from collections import OrderedDict

autocmp = OrderedDict({
    # key, search path, end node
    'AllIdAutoCmp': ('routers/table/AllIdAutoCmp.yaml', {
        'twse': ([0],),
        'otc': ([1],)
    })
})

# register your strategies here
routers = OrderedDict({
    # key, search path, init node, middle node, end node
    'StockProfileRaw': ('routers/table/StockProfileRaw.yaml', {
        'twse': ([0,1,2], [3], [4]),
        'otc': ([5,6,7], [8], [9])
        }),
    'TraderProfileRaw': ('routers/table/TraderProfileRaw.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'StockProfileUp0': ('routers/table/StockProfileUp0.yaml', {
        'twse': ([0,1,2], [3], [4]),
        'otc': ([5,6,7], [8], [9])
        }),
    'StockProfileDown0': ('routers/table/StockProfileDown0.yaml', {
        'twse': ([0,1,2], [3], [4]),
        'otc': ([5,6,7], [8], [9])
        }),
    'StockProfileUp1': ('routers/table/StockProfileUp1.yaml', {
        'twse': ([0], [1,2,3], [4]),
        'otc': ([5], [6,7,8], [9])
        }),
    'StockProfileDown1': ('routers/table/StockProfileDown1.yaml', {
        'twse': ([0], [1,2,3], [4]),
        'otc': ([5], [6,7,8], [9])
        }),
    'StockProfileUp2': ('routers/table/StockProfileUp2.yaml', {
        'twse': ([0], [1,2,3], [4]),
        'otc': ([5], [6,7,8], [9])
        }),
    'StockProfileDown2': ('routers/table/StockProfileDown2.yaml', {
        'twse': ([0], [1,2,3], [4]),
        'otc': ([5], [6,7,8], [9])
        }),
    'TraderProfileUp0': ('routers/table/TraderProfileUp0.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderProfileDown0': ('routers/table/TraderProfileDown0.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderGroup0': ('routers/table/TraderGroup0.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderGroup1': ('routers/table/TraderGroup1.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderGroup2': ('routers/table/TraderGroup2.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderGroup3': ('routers/table/TraderGroup3.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'TraderGroup4': ('routers/table/TraderGroup4.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'StockGroup0': ('routers/table/StockGroup0.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        }),
    'StockGroup1': ('routers/table/StockGroup1.yaml', {
        'twse': ([0], [], [1]),
        'otc': ([2], [], [3])
        })
})

ALG_CHOICES = [(i, k) for i, k in enumerate(sorted(routers.keys()))]

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