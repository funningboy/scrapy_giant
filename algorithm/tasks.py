# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task
from celery import chain

from handler.tasks import *
from algorithm.report import Report
from algorithm.dualema import DualEMAAlgorithm
from algorithm.randforest import RandForestAlgorithm
from algorithm.bbands import BBandsAlgorithm
from algorithm.kmeans import KmeansAlgorithm

from celery.utils.log import get_task_logger
logger = get_task_logger('algorithm')

# alg tasks sync
alg_tasks = {
    'dualema': DualEMAAlgorithm,
    'randforest': RandForestAlgorithm,
    'bbands': BBandsAlgorithm,
    'besttrader': BestTraderAlgorithm,
    'kmeans': KmeansAlgorithm
}


@shared_task
def run_algorithm(hisdb, alg, starttime, endtime, stockids, traderids):
    report = Report(
        sort=[('buy_count', False), ('sell_count', False), ('volume', False)], limit=20)
    dbhandler = hisdb_tasks[hisdb]()
    dbhandler.stock.ids = stockids
    dbhandler.trader.ids = traderids
    args = (starttime, endtime, stockids, traderids, order, limit)
    data = dbhandler.transform_all_data(*args)
    alg = alg_task[alg](dbhandler=dbhandler)
    report.collect(stockid, results)

    return alg.run(data).fillna(0)

