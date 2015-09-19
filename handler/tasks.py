# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pickle
import pandas as pd
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

hisitems = ['stock', 'credit', 'future', 'trader']
iditems = ['stock', 'trader']

@shared_task(time_limit=60*60)
def collect_iditem(stream):
    args, kwargs = pickle.loads(stream)

    opt = kwargs.pop('opt', None)
    targets = kwargs.pop('targets', [])
    callback = kwargs.pop('callback', None) 
    debug = kwargs.pop('debug', False)

    item = {}
    idhandler = iddb_tasks[opt](debug=debug)
    for target in targets:
        ptr = getattr(idhandler, target)
        dt = ptr.query_raw()
        if dt:
            item.update({target+'item': dt})

    return pickle.dumps(item)


@shared_task(time_limit=60*60)
def collect_hisitem(stream):
    args, kwargs = pickle.loads(stream)

    opt = kwargs.pop('opt', None)
    targets = kwargs.pop('targets', [])
    starttime = kwargs.pop('starttime', )
    endtime = kwargs.pop('endtime', )
    base = kwargs.pop('base', 'stock')
    constraint = kwargs.pop('constraint', None)
    order = kwargs.pop('order', None)
    stockids = kwargs.pop('stockids', [])
    traderids = kwargs.pop('traderids', [])
    limit = kwargs.pop('limit', 10)
    callback = kwargs.pop('callback', None)
    debug = kwargs.pop('debug', False)
    
    item = {}
    dbhandler = hisdb_tasks[opt](debug=debug)
    for target in targets:
        if target in hisitems:
            ptr = getattr(dbhandler, target)
            if target in ['trader']:
                args = (starttime, endtime, stockids, traderids, base, constraint, order, limit)
            else:
                args = (starttime, endtime, stockids, base, constraint, order, limit)

            dt = ptr.query_raw(*args)
            if dt:
                item.update({target+'item': dt})

    return pickle.dumps(item)


def collect_hisframe(opt, targets, starttime, endtime, base='stock', constraint=None, order=None, stockids=[], traderids=[], limit=10, callback=None, debug=False):
    """ raw his stock/toptrader/credit/future item to df
    <stockid>                                | <stockid> ...
                open| high| financeused| top0|           open | ...
    20140928    100 | 101 | 0,2        | 100 |20140928 | 110  | ...
    20140929    100 | 102 | 0.3        | 200 |20140929 | 110  | ...
    """

    group = []
    dbhandler = hisdb_tasks[opt](debug=debug)
    for target in targets:
        if target in hisitems:
            ptr = getattr(dbhandler, target)
            cb = ptr.to_pandas
            if target in ['trader']:
                ptr.ids = stockids if base == 'stock' else traderids
                args = (starttime, endtime, stockids, traderids, base, constraint, order, limit, cb)
            else:
                ptr.ids = stockids
                args = (starttime, endtime, stockids, base, constraint, order, limit, cb)

            df = ptr.query_raw(*args)
            if not df.empty:
                group.append(df)
                
    if group:
        panel = pd.concat(group, axis=2).fillna(0)
        return panel, dbhandler
        
    return pd.Panel(), dbhandler