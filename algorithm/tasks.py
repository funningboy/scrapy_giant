# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task
from handler.tasks import iddb_tasks
from algorithm.algdb_handler import *

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
def run_algorithm_service(opt, alg, starttime, endtime, debug=False):
    id = iddb_tasks[opt](debug=debug)
    id.stock.get_ids()
    id.trader.get_ids()

    alg = algdb_tasks[opt][alg](**kwargs)
    alg.run(alg.to_summary)

def collect_algframe():
    pass
