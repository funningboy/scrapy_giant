# -*- coding: utf-8 -*-

from main.models import ALG_CHOICES

DETAIL_LIMIT = 10
LIST_LIMIT = 50

def StockProfile0_buy(**collect):
    # StockProfile0+
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

def StockProfile0_sell(**collect):
    # StockProfile0-
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

def StockProfile1_buy(**collect):
    # StockProfile1+
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

def StockProfile1_sell(**collect):
    # StockProfile1-
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

def TraderProfile0_buy(**collect):
    # TraderProfile0+
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

def TraderProfile0_sell(**collect):
    # TraderProfile0-
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

def DualemaProfile(**collect):
    pass

