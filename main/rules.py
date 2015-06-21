# -*- coding: utf-8 -*-

from main.models import ALG_CHOICES

DETAIL_LIMIT = 10
LIST_LIMIT = 50

def StockProfileUp0(collect):
    if collect['algorithm'] == ALG_CHOICES[0][1]:
        G = nx.DiGraph()
        G.add_node(0, {'ptr': hisstockn})
        G.add_node(1, {'ptr': hiscreditn})
        G.add_edge
        G.add_edge(0, 1, weight=1)
        return G

def StockProfileDown0(collect):
    if collect['algorithm'] == ALG_CHOICES[1][1]:
        limit = DETAIL_LIMIT if collect['method'] == 'detail' else LIST_LIMIT
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

def StockProfileUp1(collect):
    if collect['algorithm'] == ALG_CHOICES[2][1]:
        limit = DETAIL_LIMIT if collect['method'] == 'detail' else LIST_LIMIT
        collect['frame']['hisstock'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume', '+totaldiff'],
            'limit': limit,
            'priority': 1
        })
        collect['frame']['hiscredit'].update({
            'on': True,
            'base': 'stock',
            'order': ['+bearishused', '+financeused'],
            'limit': limit,
            'priority': 0
        })
        collect['frame']['histrader'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume'],
            'limit': limit,
            'priority': 2
        })

def StockProfileDown1(collect):
    if collect['algorithm'] == ALG_CHOICES[3][1]:
        limit = DETAIL_LIMIT if collect['method'] == 'detail' else LIST_LIMIT
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
            'priority': 0
        })
        collect['frame']['histrader'].update({
            'on': True,
            'base': 'stock',
            'order': ['-totalvolume'],
            'limit': limit,
            'priority': 2
        })

def TraderProfileUp0(collect):
    if collect['algorithm'] == ALG_CHOICES[4][1]:
        limit = DETAIL_LIMIT if collect['method'] == 'detail' else LIST_LIMIT
        collect['frame']['histrader'].update({
            'on': True,
            'base': 'trader',
            'order': ['-totalvolume', '-totalbuyvolume', '+totalsellvolume'],
            'limit': limit,
            'priority': 0
        })

def TraderProfileDown0(collect):
    if collect['algorithm'] == ALG_CHOICES[5][1]:
        limit = DETAIL_LIMIT if collect['method'] == 'detail' else LIST_LIMIT
        collect['frame']['histrader'].update({
            'on': True,
            'base': 'trader',
            'order': ['-totalvolume', '-totalsellvolume', '+totalbuyvolume'],
            'limit': limit,
            'priority': 0
        })
 
