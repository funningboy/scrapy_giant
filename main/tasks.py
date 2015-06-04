# -*- coding: utf-8 -*-

from main.router import *

def is_hisstock_detail(**collect):
    router = [
        StockProfile0_buy,
        StockProfile0_sell,
        StockProfile1_buy,
        StockProfile1_sell
    ]
    if collect['algorithm'] not in [i[1] for i in ALG_CHOICES if i[0] in range(0,4)]:
        return False
    if collect['starttime'] >= collect['endtime'] or len(collect['stockids']) != 1:
        return False
    [r(**collect) for r in router]
    return True

def is_hisstock_list(**collect):
    router = [
        StockProfile0_buy,
        StockProfile0_sell,
        StockProfile1_buy,
        StockProfile1_sell
    ]
    if collect['algorithm'] not in [i[1] for i in ALG_CHOICES if i[0] in range(0,4)]:
        return False
    if collect['starttime'] >= collect['endtime']:
        return False
    [r(**collect) for r in router]
    return True

def is_histrader_detail(**collect):
    router = [
        TraderProfile0_buy,
        TraderProfile0_sell
    ]
    if collect['algorithm'] not in [i[1] for i in ALG_CHOICES if i[0] in range(4,6)]:
        return False
    if collect['starttime'] >= collect['endtime'] and len(collect['traderids']) != 1:
        return False
    [r(**collect) for r in router]
    return True

def is_histrader_list(**collect):
    router = [
        TraderProfile0_buy,
        TraderProfile0_sell
    ]
    if collect['algorithm'] not in [i[1] for i in ALG_CHOICES if i[0] in range(4,6)]:
        return False
    if collect['starttime'] >= collect['endtime']:
       return False
    [r(**collect) for r in router]
    return True
