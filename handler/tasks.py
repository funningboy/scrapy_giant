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

# as pipeline to alg service
@shared_task
def run_hisstock_query(hisdb, starttime, endtime, stockids=[], debug=False):
    if hisdb not in hisdb_tasks:
        logger.error("%s handler not support" % (hisdb))
        raise Exception
    dbhandler = hisdb_tasks[hisdb]()
    dbhandler.stock.ids = stockids
    cursor = dbhandler.stock.query(
        starttime=starttime,
        endtime=endtime,
        stockids=stockids)
    return dbhandler.stock.to_pandas(cursor)

# as pipeline to alg service
@shared_task
def run_histoptrader_query(hisdb, starttime, endtime, stockids=[], traderids=[], base='stock', opt='buy', limit=10, debug=False):
    if hisdb not in hisdb_tasks:
        logger.error("%s handler not support" % (hisdb))
        raise Exception
    dbhandler = hisdb_tasks[hisdb]()
    dbhandler.stock.ids = stockids
    dbhandler.trader.ids = traderids
    cursor = dbhandler.trader.query(
        starttime=starttime,
        endtime=endtime,
        stockids=stockids,
        traderids=traderids,
        base=base,
        opt=opt,
        limit=limit)
    return dbhandler.trader.to_pandas(cursor)

# as pipeline to alg service
@shared_task
def run_transform_all_data(hisdb, starttime, endtime, stockids=[], traderids=[], base='stock', opt='buy', limit=10, debug=False):
    if hisdb not in hisdb_tasks:
        logger.error("%s handler not support" % (hisdb))
        raise Exception
    dbhandler = hisdb_tasks[hisdb]()
    dbhandler.stock.ids = stockids
    dbhandler.trader.ids = traderids
    dbhandler.transform_all_data()
    panel = dbhandler.transform_all_data(starttime, endtime, stockids, traderids, limit)
    return panel
