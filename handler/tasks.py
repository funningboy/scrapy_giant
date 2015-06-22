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

    item = {
        'stockitem': None,
        'traderitem': None,
        'credititem': None,
        'futureitem': None
    }
    
    assert(opt in ['twse', 'otc'])
    assert(target in ['stock', 'trader', 'credit', 'future', 'all'])
   
    idhandler = iddb_tasks[opt](debug=debug)
    dbhandler = hisdb_tasks[opt](debug=debug)

    if target in ['stock', 'all']:
        args = (starttime, endtime, stockids, base, order, limit)
        dt = dbhandler.stock.query_raw(*args)
        if dt:
            item.update({'stockitem': dt})

    if target in ['credit', 'all']:
        args = (starttime, endtime, stockids, base, order, limit)
        dt = dbhandler.credit.query_raw(*args)
        if dt:
            item.update({'credititem': dt})

    if target in ['trader', 'all']:
        args = (starttime, endtime, stockids, traderids, base, order, limit)
        dt = dbhandler.trader.query_raw(*args)
        if dt:
            item.update({'traderitem': dt})

    if target in ['future', 'all']:
        pass
        #args = (starttime, endtime, stockids, base, order, limit)
        #dt = dbhandler.future.query_raw(*args)
        #if dt:
        #    item.update({'futureitem': dt})
   
    return item, dbhandler


def collect_hisframe(collect):
    """  as middleware collect raw his stock/toptrader/credit/future to df
    <stockid>                                | <stockid> ...
                open| high| financeused| top0|           open | ...
    20140928    100 | 101 | 0,2        | 100 |20140928 | 110  | ...
    20140929    100 | 102 | 0.3        | 200 |20140929 | 110  | ...
    """

    if 'debug' in collect and collect['debug']:
        print json.dumps(dict(collect), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)

    group = []
    opt = collect['opt']
    assert(opt in ['twse', 'otc'])
    frame = collect['frame']
    cols = frame.keys()
    assert(cols <= ['hisstock', 'histrader', 'hiscredit', 'hisfuture'])
    assert(len(set([frame[col]['base'] for col in cols if frame[col]['on']]))==1)

    dbhandler = hisdb_tasks[opt](**collect)
    for it in frame:
        if it == 'hisstock':
            if frame[it]['on']:
                frame[it].pop('on')
                dbhandler.stock.ids = frame[it]['stockids']
                frame[it].update({'callback': dbhandler.stock.to_pandas})
                frame[it].pop('priority')
                df = dbhandler.stock.query_raw(**frame[it])
                if not df.empty:
                    group.append(df)
        if it == 'histrader':
            if frame[it]['on']:
                frame[it].pop('on')
                dbhandler.trader.ids = frame[it]['stockids']
                frame[it].update({'callback': dbhandler.trader.to_pandas})
                frame[it].pop('priority')
                df = dbhandler.trader.query_raw(**frame[it])
                if not df.empty:
                    group.append(df)
        if it == 'hiscredit':
            if frame[it]['on']:
                frame[it].pop('on')
                dbhandler.credit.ids = frame[it]['stockids']
                frame[it].update({'callback': dbhandler.credit.to_pandas})
                frame[it].pop('priority')
                df = dbhandler.credit.query_raw(**frame[it])
                if not df.empty:
                    group.append(df)
        if it == 'hisfuture':
            if frame[it]['on']:
                frame[it].pop('on')
                dbhandler.future.ids = frame[it]['stockids']
                frame[it].update({'callback': dbhandler.future.to_pandas})
                frame[it].pop('priority')
                df = dbhandler.future.query_raw(**frame[it])
                if not df.empty:
                    group.append(df)
    if group:
        panel = pd.concat(group, axis=2).fillna(0)
        return panel, dbhandler
    return pd.Panel(), dbhandler

def collect_relitem(collect):
    pass

def collect_relframe(collect):
    pass
