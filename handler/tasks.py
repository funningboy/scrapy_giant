# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pandas as pd
import json
from bson import json_util
from celery import shared_task
from datetime import datetime, timedelta
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler

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


def collect_hisitem(**kwargs):
    """ as middleware cascade collect raw hisstock/histoptrader/hiscredit to item
    filer priority 0>1>2
    """
    collect = {
        'hisstock': {
            'on': False,
            'starttime': datetime.utcnow() - timedelta(days=100),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'base': 'stock',
            'order': ['-totalvolume', '-totaldiff'],
            'callback': None,
            'limit': 10,
            'priority': 0
        },
        'hiscredit': {
            'on': False,
            'starttime': datetime.utcnow() - timedelta(days=100),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'base': 'stock',
            'order': ['-financeused', '-bearishused'],
            'callback': None,
            'limit': 10,
            'priority': 1
        },
        'histrader': {
            'on': False,
            'starttime': datetime.utcnow() - timedelta(days=10),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'traderids':[],
            'base': 'stock',
            'order': ['-totalvolume'],
            'callback': None,
            'limit': 10,
            'priority': 2,
        }
   }
    item = {}
    #populate to each query kwargs/constrain
    opt = kwargs['opt']
    assert(opt in ['twse', 'otc'])
    cols = kwargs['frame'].keys()
    assert(cols <= ['hisstock', 'histrader', 'hiscredit'])
    for col in cols:
        assert(set(collect[col].keys()) >= set(kwargs['frame'][col].keys()))
        collect[col].update(**kwargs['frame'][col])
        collect[col]['on'] = True
    assert(len(set([collect[col]['base'] for col in cols if collect[col]['on']]))==1)

    stockids = []
    [stockids.extend(collect[col]['stockids']) for col in cols if collect[col]['on']]
    stockids = list(set(stockids))

    traderids = []
    [traderids.extend(collect[col]['traderids']) for col in ['histrader'] if collect[col]['on'] and collect[col]['traderids']]
    traderids = list(set(traderids))

    if 'debug' in kwargs and kwargs['debug']:
        print json.dumps(dict(collect), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)

    dbhandler = hisdb_tasks[opt](**kwargs)
    for it, p in sorted(collect.items(), key=lambda x: x[1]['priority']):
        if it == 'hisstock':
            if collect[it]['on']:
                [collect[it].pop(k) for k in ['on', 'priority']]
                collect[it]['stockids'] = stockids
                dt = dbhandler.stock.query_raw(**collect[it])
                if dt:
                    item.update({'stockitem': dt})
                    stockids = [i['stockid'] for i in dt]
        if it == 'hiscredit':
            if collect[it]['on']:
                [collect[it].pop(k) for k in ['on', 'priority']]
                collect[it]['stockids'] = stockids
                dt = dbhandler.credit.query_raw(**collect[it])
                if dt:
                    item.update({'credititem': dt})
                    stockids = [i['stockid'] for i in dt]
        if it == 'histrader':
            if collect[it]['on']:
                [collect[it].pop(k) for k in ['on', 'priority']]
                collect[it]['stockids'] = stockids
                collect[it]['traderids'] = traderids
                dt = dbhandler.trader.query_raw(**collect[it])
                if dt:
                    item.update({'traderitem': dt})
                    stockids = [i['stockid'] for i in dt]
                    traderids = [i['traderid'] for i in dt]

    return item, dbhandler


def collect_hisframe(**kwargs):
    """  as middleware collect raw hisstock/histoptrader/hiscredit to df
    <stockid>                                | <stockid> ...
                open| high| financeused| top0|           open | ...
    20140928    100 | 101 | 0,2        | 100 |20140928 | 110  | ...
    20140929    100 | 102 | 0.3        | 200 |20140929 | 110  | ...
    """
    collect = {
        'hisstock': {
            'on': False,
            'starttime': datetime.utcnow() - timedelta(days=100),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'base': 'stock',
            'order': ['-totalvolume', '-totaldiff'],
            'callback': None,
            'limit': 10
        },
        'histrader': {
            'on': False,
            'starttime': datetime.utcnow() - timedelta(days=10),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'traderids':[],
            'base': 'stock',
            'order': ['-totalvolume'],
            'callback': None,
            'limit': 10
        },
        'hiscredit': {
            'on': False,
            'starttime': datetime.utcnow() - timedelta(days=100),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'base': 'stock',
            'order': ['-financeused', '-bearishused'],
            'callback': None,
            'limit': 10
        }
    }
    group = []
    #populate to each query kwargs/constrain
    opt = kwargs['opt']
    assert(opt in ['twse', 'otc'])
    cols = kwargs['frame'].keys()
    assert(cols <= ['hisstock', 'histrader', 'hiscredit'])
    for col in cols:
        assert(set(collect[col].keys()) >= set(kwargs['frame'][col].keys()))
        collect[col].update(**kwargs['frame'][col])
        collect[col]['on'] = True
    assert(len(set([collect[col]['base'] for col in cols if collect[col]['on']]))==1)

    if 'debug' in kwargs and kwargs['debug']:
        print json.dumps(dict(collect), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)

    dbhandler = hisdb_tasks[opt](**kwargs)
    for it in collect:
        if it == 'hisstock':
            if collect[it]['on']:
                collect[it].pop('on')
                dbhandler.stock.ids = collect[it]['stockids']
                collect[it].update({'callback': dbhandler.stock.to_pandas})
                df = dbhandler.stock.query_raw(**collect[it])
                if not df.empty:
                    group.append(df)
                    print df['2317']
        if it == 'histrader':
            if collect[it]['on']:
                collect[it].pop('on')
                dbhandler.trader.ids = collect[it]['stockids']
                collect[it].update({'callback': dbhandler.trader.to_pandas})
                df = dbhandler.trader.query_raw(**collect[it])
                if not df.empty:
                    group.append(df)
                    print df['2317']
        if it == 'hiscredit':
            if collect[it]['on']:
                collect[it].pop('on')
                dbhandler.credit.ids = collect[it]['stockids']
                collect[it].update({'callback': dbhandler.credit.to_pandas})
                df = dbhandler.credit.query_raw(**collect[it])
                if not df.empty:
                    group.append(df)
                    print df['2317']
    if group:
        panel = pd.concat(group, axis=2).fillna(0)
        return panel, dbhandler
    return pd.Panel(), dbhandler

def collect_relframe(**kwargs):
    pass
