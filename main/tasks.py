# -*- coding: utf-8 -*-

from main.router import *

def is_hisstock_detail(**collect):
    router = [
        StockProfileUp0,
        StockProfileDown0,
        StockProfileUp1,
        StockProfileDown1
    ]
    if collect['algorithm'] not in [i[1] for i in ALG_CHOICES if i[0] in range(0,4)]:
        return False
    if collect['starttime'] >= collect['endtime'] or len(collect['stockids']) != 1:
        return False
    collect.update({'type': 'detail'})
    [r(**collect) for r in router]
    return True

def is_hisstock_list(**collect):
    router = [
        StockProfileUp0,
        StockProfileDown0,
        StockProfileUp1,
        StockProfileDown1
    ]
    if collect['algorithm'] not in [i[1] for i in ALG_CHOICES if i[0] in range(0,4)]:
        return False
    if collect['starttime'] >= collect['endtime']:
        return False
    collect.update({'type': 'list'})
    [r(**collect) for r in router]
    return True

def is_histrader_detail(**collect):
    router = [
        TraderProfileUp0,
        TraderProfileDown0
    ]
    if collect['algorithm'] not in [i[1] for i in ALG_CHOICES if i[0] in range(4,6)]:
        return False
    if collect['starttime'] >= collect['endtime'] and len(collect['traderids']) != 1:
        return False
    collect.update({'type': 'detail'})
    [r(**collect) for r in router]
    return True

def is_histrader_list(**collect):
    router = [
        TraderProfileUp0,
        TraderProfileDown0
    ]
    if collect['algorithm'] not in [i[1] for i in ALG_CHOICES if i[0] in range(4,6)]:
        return False
    if collect['starttime'] >= collect['endtime']:
       return False
    collect.update({'type': 'list'})
    [r(**collect) for r in router]
    return True
