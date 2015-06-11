# -*- coding: utf-8 -*-

from main.models import ALG_CHOICES

DETAIL_LIMIT = 10
LIST_LIMIT = 50

def StockProfileUp0(**collect):
    if collect['algorithm'] == ALG_CHOICES[0][1]:
        limit = DETAIL_LIMIT if collect['type'] == 'detail' else LIST_LIMIT
        collect['frame']['hisstock'].update({
            'on': True,
            'base': 'stock',
            'order': ['+totaldiff', '-totalvolume'],
            'limit': limit,
            'priority': 0
        })
        collect['frame']['hiscredit'].update({
            'on': True,
            'base': 'stock',
            'order': ['+financeused', '+bearishused'],
            'limit': limit,
            'priority': 1
        })
        collect['frame']['histrader'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume'],
            'limit': limit,
            'priority': 2
        })

def StockProfileDown0(**collect):
    if collect['algorithm'] == ALG_CHOICES[1][1]:
        limit = DETAIL_LIMIT if collect['type'] == 'detail' else LIST_LIMIT
        collect['frame']['hisstock'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totaldiff', '-totalvolume'],
            'limit': limit,
            'priority': 0
        })
        collect['frame']['hiscredit'].update({
            'on': True,
            'base': 'stock',
            'order': ['-bearishused', '-financeused'],
            'limit': limit,
            'priority': 1
        })
        collect['frame']['histrader'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume'],
            'limit': limit,
            'priority': 2
        })

def StockProfileUp1(**collect):
    if collect['algorithm'] == ALG_CHOICES[2][1]:
        limit = DETAIL_LIMIT if collect['type'] == 'detail' else LIST_LIMIT
        collect['frame']['hisstock'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume', '+totaldiff'],
            'limit': limit,
            'priority': 0
        })
        collect['frame']['hiscredit'].update({
            'on': True,
            'base': 'stock',
            'order': ['+bearishused', '+financeused'],
            'limit': limit,
            'priority': 1
        })
        collect['frame']['histrader'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume'],
            'limit': limit,
            'priority': 2
        })

def StockProfileDown1(**collect):
    if collect['algorithm'] == ALG_CHOICES[3][1]:
        limit = DETAIL_LIMIT if collect['type'] == 'detail' else LIST_LIMIT
        collect['frame']['hisstock'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume', '-totaldiff'],
            'limit': limit,
            'priority': 0
        })
        collect['frame']['hiscredit'].update({
            'on': True,
            'base': 'stock',
            'order': ['-bearishused', '-financeused'],
            'limit': limit,
            'priority': 1
        })
        collect['frame']['histrader'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume'],
            'limit': limit,
            'priority': 2
        })

def TraderProfileUp0(**collect):
    if collect['algorithm'] == ALG_CHOICES[4][1]:
        limit = DETAIL_LIMIT if collect['type'] == 'detail' else LIST_LIMIT
        collect['frame']['histrader'].update({
            'on': True,
            'base': 'trader',
            'order': ['-totalvolume'],
            'limit': limit,
            'priority': 0
        })
        collect['frame']['hisstock'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume', '-totaldiff'],
            'limit': limit,
            'priority': 1
        })
        collect['frame']['hiscredit'].update({
            'on': True,
            'base': 'stock',
            'order': ['+financeused', '+bearishused'],
            'limit': limit,
            'priority': 2
        })

def TraderProfileDown0(**collect):
    if collect['algorithm'] == ALG_CHOICES[5][1]:
        limit = DETAIL_LIMIT if collect['type'] == 'detail' else LIST_LIMIT
        collect['frame']['histrader'].update({
            'on': True,
            'base': 'trader',
            'order': ['-totalvolume'],
            'limit': limit,
            'priority': 0
        })
        collect['frame']['hisstock'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume', '-totaldiff'],
            'limit': limit,
            'priority': 1
        })
        collect['frame']['hiscredit'].update({
            'on': True,
            'base': 'stock',
            'order': ['-bearishused', '-financeused'],
            'limit': limit,
            'priority': 2
        })

def DualemaProfileUp0(**collect):
    pass

def DualemaProfileDown0(**collect):
    pass

