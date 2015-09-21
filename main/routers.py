# -*- coding: utf-8 -*-

from main.models import *
import re

def is_hisstock_detail(collect):
    stocks = zip(*filter(lambda x: re.match('stock', str(x[1]).lower()), list(ALG_CHOICES)))[1]
    if collect['algorithm'] in stocks:
        if len(collect['stockids']) == 1:
            return True

def is_hisstock_list(collect):
    stocks = zip(*filter(lambda x: re.match('stock', str(x[1]).lower()), list(ALG_CHOICES)))[1]
    if collect['algorithm'] in stocks:
        return True

def is_histrader_detail(collect):
    traders = zip(*filter(lambda x: re.match('trader', str(x[1]).lower()), list(ALG_CHOICES)))[1]
    if collect['algorithm'] in traders:
        if len(collect['traderids']) == 1:
            return True

def is_histrader_list(collect):
    traders = zip(*filter(lambda x: re.match('trader', str(x[1]).lower()), list(ALG_CHOICES)))[1]
    if collect['algorithm'] in traders:
        return True

def is_teststock_detail(collect):
    stocks = zip(*filter(lambda x: re.match('teststock', str(x[1]).lower()), list(ALG_CHOICES)))[1]
    if collect['algorithm'] in stocks:
        if len(collect['stockids']) == 1:
            return True

def is_teststock_list(collect):
    stocks = zip(*filter(lambda x: re.match('teststock', str(x[1]).lower()), list(ALG_CHOICES)))[1]
    if collect['algorithm'] in stocks:
        return True

def is_testtrader_list(collect):
    stocks = zip(*filter(lambda x: re.match('testtrader', str(x[1]).lower()), list(ALG_CHOICES)))[1]
    if collect['algorithm'] in stocks:
        return True

def is_testtrader_detail(collect):
    traders = zip(*filter(lambda x: re.match('testtrader', str(x[1]).lower()), list(ALG_CHOICES)))[1]
    if collect['algorithm'] in traders:
        if len(collect['traderids']) == 1:
            return True