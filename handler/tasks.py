# -*- coding: utf-8 -*-

from __future__ import absolute_import

#from main.celery import app
from celery import shared_task

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

def trans_hisframe(opt, starttime, endtime, stockids=[], traderids=[], base='stock', order=['totalvolume']*3, limit=10, debug=False):
    """  as middleware trans raw hisstock/histoptrader/hiscredit to df
    order[0:3] : [stock, trader, credit] 
    """
    kwargs = {
        'opt': opt,
        'debug': debug
    }
    db = hisdb_tasks[opt](**kwargs)
    group = []
    if base == 'stock':
        for i, k in enumerate(order):
            if i == 0 and k not None:
                db.stock.ids = stockids
                args = (starttime, endtime, stockids, order[0], limit, db.stock.to_pandas)
                group.append(db.stock.query_raw(*args))
            elif i == 1 and k not None:
                db.trader.ids = stockids 
                args = (starttime, endtime, stockids, traderids, base, order[1], limit, db.trader.to_pandas)
                group.append(db.trader.query_raw(*args))
            elif i == 2 and k not None:
                db.credit.ids = stockids
                args = (starttime, endtime, stockids, order[2], limit, db.credit.to_pandas)
                group.append(db.credit.query_raw(*args))
    elif base == 'trader':
        for i, k in enumerate(order):
            if i == 1 and k not None:
                db.trader.ids = traderids
                args = (starttime, endtime, stockids, traderids, base, order[1], limit, db.trader.to_pandas)
                group.append(db.trader.query_raw(*args))
    if group:
    panel = pd.concat(group, inx=2)
    return panel, db

def trans_relframe():
    pass
