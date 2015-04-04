# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task
from celery import chain

from handler.tasks import *
from algorithm.report import Report
from algorithm.dualema import DualEMAAlgorithm
from algorithm.randforest import RandForestAlgorithm
from celery.utils.log import get_task_logger
logger = get_task_logger('algorithm')

# alg tasks sync
alg_tasks = {
    'dualema': DualEMAAlgorithm,
    'randforest': RandForestAlgorithm,
#    'bbands': BBandsAlgorithm
}


@shared_task
def run_algorithm(hisdb, alg, starttime, endtime, ):
    dbhandler = hisdb_tasks[hisdb]()
    dbhandler.stockids =
    dbhandler.traderids =
    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    dd = endtime - starttime
    maxlen = 30
    if dd.days < maxlen:
        return
    args = (starttime, endtime, [stockid], order, limit)
    data = dbhandler.transform_all_data(*args)
    if len(data[stockid].index) < maxlen:
        return
    alg = alg_task[alg](dbhandler=dbhandler)
    results = alg.run(data).fillna(0)
    return stockid, results

