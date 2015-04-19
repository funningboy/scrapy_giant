# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task

from algorithm.algdb_handler import *
from handler.tasks import iddb_tasks

from celery.utils.log import get_task_logger
logger = get_task_logger('algorithm')

algdb_tasks = {
        'twse': {
            'dualema': TwseDualemaAlg,
            'btrader': TwseBestTraderAlg,
            'bbands': TwseBBandsAlg,
            'rforest': TwseRandForestAlg
            },
        'otc': {
            'dualema': OtcDualemaAlg,
            'btrader': OtcBestTraderAlg,
            'bbands': OtcBBandsAlg,
            'rforest': OtcRandForestAlg
            }
}

# as background service
@shared_task
def run_algorithm_service(opt, alg, starttime, endtime, limit=10, debug=False):
    idhandler = iddb_tasks[opt]()
    stockids =[id for id in idhandler.stock.get_ids(limit, debug, opt)]
    traderids = [id for id in idhandler.trader.get_ids(limit, debug, opt)]
    alg = algdb_tasks[opt][alg]()
    args = (starttime, endtime, stockids, traderids, 'totalvolume', limit, alg.to_summary)
    alg.run(*args)
