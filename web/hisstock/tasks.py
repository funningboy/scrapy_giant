# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery import shared_task

from bin.logger import Logger
from query.hisdb_query import (TwseHisDBQuery, OtcHisDBQuery)

hisdb_tasks = {
    'twse': TwseHisDBQuery,
    'otc': OtcHisDBQuery
}

@shared_task(name='web.hisdbapp.tasks.run_hisdb_stock_query')
def run_hidb_stock_query(hisdb, starttime, endtime, stockids=[],
    traderids=[], debug=False):
    if hisdb not in hisdb_tasks:
        Logger.error("%s hisdb not support" % (hisdb))
        raise Exception
    dbquery = hisdb_tasks[hisdb]()
    data = dbquery.get_all_data(
        starttime=starttime,
        endtime=endtime,
        stockids=stockids,
        traderids=traderids
    )
    return data

@shared_task(name='web.hisdbapp.tasks.run_hisdb_trader_query')
def run_hisdb_trader_query(hisdb, starttime, endtime, stockids=[],
    traderids=[], dtyp='buy', limit=10, debug=False):
    if hisdb not hisdb_tasks:
        Logger.error("%s hisdb not support" % (hisdb))
        raise Exception
    dbquery = hisdb_tasks[hisdb]()
    data = dbquery.get_toptrader_data(
        starttime=starttime,
        endtime=endtime,
        stockids=stockids,
        traderids=traderids,
        opt='trader',
        dtyp=dtyp,
        limit=limit
    )
    return data
