# -*- coding: utf-8 -*-

import pandas as pd
import json
from bson import json_util
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler

from giant.celery import app
from celery import shared_task

from celery.utils.log import get_task_logger
logger = get_task_logger('handler')

hisdb_tasks = {
    'twse': TwseHisDBHandler,
    'otc': OtcHisDBHandler
}

iddb_tasks = {
    'twse': TwseIdDBHandler,
    'otc': OtcIdDBHandler
}

@shared_task
def collect_hisitem(opt, target, starttime, endtime, base='stock', order=[], stockids=[], traderids=[], limit=10, callback=None, debug=False):
    """ as middleware collect raw his stock/toptrader/credit/future to item
    """

    assert(opt in ['twse', 'otc'])
    assert(target in ['stock', 'trader', 'credit', 'future', 'itemall'])
    assert(base in ['stock', 'trader'])
    #asssert ...

    item = {
        'stockitem': [],
        'traderitem': [],
        'credititem': [],
        'futureitem': []
    }
    
    idhandler = iddb_tasks[opt](debug=debug)
    dbhandler = hisdb_tasks[opt](debug=debug)

    if target in ['stock', 'itemall']:
        args = (starttime, endtime, stockids, base, order, limit)
        dt = dbhandler.stock.query_raw(*args)
        if dt:
            item.update({'stockitem': dt})

    if target in ['credit', 'itemall']:
        args = (starttime, endtime, stockids, base, order, limit)
        dt = dbhandler.credit.query_raw(*args)
        if dt:
            item.update({'credititem': dt})

    if target in ['trader', 'itemall']:
        args = (starttime, endtime, stockids, traderids, base, order, limit)
        dt = dbhandler.trader.query_raw(*args)
        if dt:
            item.update({'traderitem': dt})

    if target in ['future', 'itemall']:
        args = (starttime, endtime, stockids, base, order, limit)
        dt = dbhandler.future.query_raw(*args)
        if dt:
            item.update({'futureitem': dt})
   
    return item


def collect_hisframe(opt, target, starttime, endtime, base='stock', order=[], stockids=[], traderids=[], limit=10, callback=None, debug=False):
    """  as middleware collect raw his stock/toptrader/credit/future to df
    <stockid>                                | <stockid> ...
                open| high| financeused| top0|           open | ...
    20140928    100 | 101 | 0,2        | 100 |20140928 | 110  | ...
    20140929    100 | 102 | 0.3        | 200 |20140929 | 110  | ...
    """

    group = []
    assert(opt in ['twse', 'otc'])
    assert(target in ['stock', 'trader', 'credit', 'future', 'itemall'])
    #assert stockids, traderids
    #assert ...

    dbhandler = hisdb_tasks[opt](debug=debug)

    if target in ['stock', 'itemall']:
        dbhandler.stock.ids = stockids
        args = (starttime, endtime, stockids, base, order, limit, dbhandler.stock.to_pandas)
        df = dbhandler.stock.query_raw(*args)
        if not df.empty:
            group.append(df)

    if target in ['credit', 'itemall']:
        dbhandler.credit.ids = stockids
        args = (starttime, endtime, stockids, base, order, limit, dbhandler.credit.to_pandas)
        df = dbhandler.credit.query_raw(*args)
        if not df.empty:
            group.append(df)

    if target in ['trader', 'itemall']:
        dbhandler.trader.ids = stockids if base == 'stock' else traderids
        args = (starttime, endtime, stockids, traderids, base, order, limit, dbhandler.trader.to_pandas)
        df = dbhandler.trader.query_raw(*args)
        if not df.empty:
            group.append(df)
        
    if target in ['future', 'itemall']:
        dbhandler.future.ids = stockids    
        args = (starttime, endtime, stockids, base, order, limit, dbhandler.futureto_pandas)
        df = dbhandler.future.query_raw(*args)
        if not df.empty:
            group.append(df)

    if group:
        panel = pd.concat(group, axis=2).fillna(0)
        return panel, dbhandler
    return pd.Panel(), dbhandler

