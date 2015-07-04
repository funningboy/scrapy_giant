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
            #'rforest': TwseRandForestAlg
            },
        'otc': {
            'dualema': OtcDualemaAlg,
            'btrader': OtcBestTraderAlg,
            'bbands': OtcBBandsAlg,
            #'rforest': OtcRandForestAlg
            }
}

# run as background services

@shared_task
def run_algitem(opt, targets, starttime, endtime, base='stock', order=[], stockids=[], traderids=[], limit=10, cfg={}, callback=None, debug=False):
    # assert ...

    for target in targets:
        kwargs = {
            'opt': opt,
            'starttime': starttime,
            'endtime': endtime,
            'base': base,
            'stockids': stockids,
            'traderids': traderids,
            'order': order,
            'constraint': constraint,
            'limit': limit,
            'cfg': cfg,
            'debug': debug
        }
        if target in ['dualema', 'btrader', 'bbands']:
            alghandler = algdb_tasks[opt][target](**kwargs) 
            dt = alghandler.run(alghandler.to_detail)
            if dt:
                item.update({target+'item': dt})
    return item

@shared_task
def collect_algitem(opt, targets, starttime, endtime, base='stock', order=[], stockids=[], traderids=[], limit=10, cfg={}, callback=None, debug=False):
    # assert ...

    item = {}

    for target in targets:
        kwargs = {
            'opt': opt,
            'starttime': starttime,
            'endtime': endtime,
            'base': base,
            'stockids': stockids,
            'traderids': traderids,
            'order': order,
            'limit': limit,
            'cfg': cfg,
            'debug': debug
        }
        if target in ['dualema', 'btrader', 'bbands']:
            alghandler = algdb_tasks[opt][target](**kwargs) 
            dt = alghandler.run(alghandler.to_detail)
            if dt:
                item.update({target+'item': dt})
    return item

