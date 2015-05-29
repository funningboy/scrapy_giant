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

def collect_hisframe(**kwargs):
    """  as middleware collect raw hisstock/histoptrader/hiscredit to df
    """
    collect = {
        # hisstock frame collect
        'hisstock': {
            'on': False,
            # hisstock query_raw
            'starttime': datetime.utcnow() - timedelta(days=100),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'order': 'totalvolume',
            'callback': None,
            'limit': 10
        },
        # histrader frame collect
        'histrader': {
            'on': False,
            # histrader query_raw
            'starttime': datetime.utcnow() - timedelta(days=10),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'traderids':[],
            'base': 'stock',
            'order': 'totalvolume',
            'callback': None,
            'limit': 10
        },
        # hiscredit frame collect
        'hiscredit': {
            'on': False,
            # hiscredit query_raw
            'starttime': datetime.utcnow() - timedelta(days=100),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'order': 'decfinance',
            'callback': None,
            'limit': 10
        }
        # hisfuture frame collect
    }
    if 'debug' in kwargs and kwargs['debug']:
        print json.dumps(dict(kwargs), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
    group = []
    #populate to each query kwargss
    opt = kwargs['opt']
    assert(opt in ['twse', 'otc'])
    cols = kwargs['frame'].keys()
    assert(cols <= ['hisstock', 'histrader', 'hiscredit'])
    for col in cols:
        assert(set(collect[col].keys()) >= set(kwargs['frame'][col].keys()))
        collect[col].update(**kwargs['frame'][col])
        collect[col]['on'] = True

    dbhandler = hisdb_tasks[opt](**kwargs)
    for it in collect:
        # collect hisstock df
        if it == 'hisstock':
            if collect[it]['on']:
                collect[it].pop('on')
                dbhandler.stock.ids = collect[it]['stockids']
                collect[it].update({'callback': dbhandler.stock.to_pandas})
                df = dbhandler.stock.query_raw(**collect[it])
                if not df.empty:
                    group.append(df)
        # collect histrader df
        if it == 'histrader':
            if collect[it]['on']:
                collect[it].pop('on')
                assert(collect[it]['base'] == 'stock')
                dbhandler.trader.ids = collect[it]['stockids']
                collect[it].update({'callback': dbhandler.trader.to_pandas})
                df = dbhandler.trader.query_raw(**collect[it])
                if not df.empty:
                    group.append(df)
        # collect hiscredit df
        if it == 'hiscredit':
            if collect[it]['on']:
                collect[it].pop('on')
                dbhandler.credit.ids = collect[it]['stockids']
                collect[it].update({'callback': dbhandler.credit.to_pandas})
                df = dbhandler.credit.query_raw(**collect[it])
                if not df.empty:
                    group.append(df)
    if group:
        panel = pd.concat(group, axis=2).fillna(0)
        return panel, dbhandler
    return pd.Panel(), dbhandler

def collect_relframe(**kwargs):
    pass
