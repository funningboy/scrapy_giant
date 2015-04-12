# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task
from celery import chain

from algorithm.algdb_handler import *

from celery.utils.log import get_task_logger
logger = get_task_logger('algorithm')

algdb_tasks = {
    'twsedualem': TwseDualemaAlg,
    'otcdualem': OtcDualemaAlg,
    'twsebtrader': TwseBestTraderAlg,
    'otcbtrader': OtcBestTraderAlg,
    'twsebbands': TwseBBandsAlg,
    'otcbbands': OtcBBandsAlg,
    'twserforest': TwseRandForestAlg,
    'otcrforest': OtcRandForestAlg
}

from bin.start import *

@shared_task
def run_algorithm_service(opt, alg, starttime, endtime, limt=10, debug=False):
    idhandler = iddb_tasks[opt]()
    stockids =[id for id in idhandler.stock.get_ids(limit, debug, opt)]
    traderids = [id for id in idhandler.trader.get_ids(limit, debug, opt)]
    args = (starttime, endtime, stockids, traderids, 'totalvolume', limit, alg.to_summary)
    alg = algdb_tasks[alg]()
    alg.run(*args)
