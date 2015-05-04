# -*- coding: utf-8 -*-

from __future__ import absolute_import

#from main.celery import app
from celery import shared_task

from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler

from celery.utils.log import get_task_logger
logger = get_task_logger('handler')

# handler tasks sync
hisdb_tasks = {
    'twse': TwseHisDBHandler,
    'otc': OtcHisDBHandler
}

iddb_tasks = {
    'twse': TwseIdDBHandler,
    'otc': OtcIdDBHandler
}

# as middleware trans raw db to df/panel
@shared_task
def trans_hisstock(opt, starttime, endtime, stockids=[], order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[opt]()
    dbhandler.stock.ids = stockids
    args = (starttime, endtime, stockids, order, limit)
    cursor = dbhandler.stock.query(*args)
    panel = dbhandler.stock.to_pandas(cursor)
    return panel, dbhandler

@shared_task
def trans_histoptrader(opt, starttime, endtime, stockids=[], traderids=[], base='stock', order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[opt]()
    dbhandler.stock.ids = stockids
    dbhandler.trader.ids = traderids
    args = (starttime, endtime, stockids, traderids, base, order, limit)
    cursor = dbhandler.trader.query(*args)
    panel = dbhandler.trader.to_pandas(cursor, base)
    return panel, dbhandler

@shared_task
def trans_hiscredit(opt, starttime, endtime, stockids=[], order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[opt]()
    dbhandler.stock.ids = stockids
    args = (starttime, endtime, stockids, order, limit)
    cursor = dbhandler.stock.query(*args)
    panel = dbhandler.credit.to_pandas(cursor)
    return panel, dbhandler

