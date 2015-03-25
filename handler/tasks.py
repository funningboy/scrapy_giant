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

# as pipeline to alg service
# chain(
# query_hisstock.s(*args),
# trans_hisstock.s()
#).apply_async().get()
@shared_task
def query_hisstock(hisdb, starttime, endtime, stockids=[], order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[hisdb]()
    dbhandler.stock.ids = stockids
    args = (starttime, endtime, stockids, order, limit)
    cursor = dbhandler.stock.query(*args)
    return hisdb, cursor

@shared_task
def trans_hisstock(hisdb, cursor):
    dbhandler = hisdb_tasks[hisdb]()
    panel = dbhandler.stock.to_pandas(cursor)
    return panel

# as pipeline to alg service
# chain(
# query_histoptrader.s(*args),
# trans_histoptrader.s()
#).apply_async().get()
@shared_task
def query_histoptrader(hisdb, starttime, endtime, stockids=[], traderids=[], base='stock', order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[hisdb]()
    dbhandler.stock.ids = stockids
    dbhandler.trader.ids = traderids
    args = (starttime, endtime, stockids, traderids, base, order, limit)
    cursor = dbhandler.trader.query(*args)
    return hisdb, cursor

@shared_task
def trans_histoptrader(hisdb, cursor):
    dbhandler = hisdb_tasks[hisdb]()
    panel = dbhandler.trader.to_pandas(cursor)
    return panel
