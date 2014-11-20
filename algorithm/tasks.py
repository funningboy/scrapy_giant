# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task

from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler

from algorithm.report import Report
from algorithm.dualema_algorithm import DualEMATaLib
from algorithm.superman_algorithm import SuperManAlgorithm
from algorithm.zombie_algorithm import ZombieAlgorithm

from celery.utils.log import get_task_logger
logger = get_task_logger('handler')

# alg tasks sync
alg_tasks = {
    'superman': SuperManAlgorithm,
    'zombie': ZombieAlgorithm,
    'dualema': DualEMATaLib
}

## as alg service,input from query task output
#@shared_task
#def run_algorithm_service(data, dbhandler, debug=False):
#    if alg not in alg_tasks:
#        Logger.error("%s algoritm not support" % (alg))
#        raise Exception
#    alg = alg_tasks[alg](dbhandler)
#    results = alg.run(data).dropna()
#    return results
#
## as report service, input from alg results
#@celery.task(name='algorithm.tasks.run_report_service')
#def run_report_service(alg, results, stockids=[], traderids=[]):
#    report = Report(
#        algname=SuperManAlgorithm.__name__,
#        sort=[('buy_count', False), ('sell_count', False), ('volume', False)], limit=20)
#    report.collect(stockid, results)
#    stream = report.summary(dtype='html')
#    report.write(stream, 'superman.html')
#    for stockid in report.iter_stockid():
#        stream = report.iter_report(stockid, dtype='html', has_other=True, has_sideband=True)
#        report.write(stream, "superman_%s.html" % (stockid))
