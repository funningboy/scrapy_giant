# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task
from handler.tasks import *
from algorithm.algdb_handler import *

from celery.utils.log import get_task_logger
logger = get_task_logger('algorithm')

algdb_tasks = {
    'twse': {
        'dualema': TwseDualemaAlg,
        'btrader': TwseBestTraderAlg,
        'bbands': TwseBBandsAlg,
        #'rforest': TwseRandForestAlg,
        #'kmeans': TwseKmeansAlg,
        #'kdtree': TwseKdTreeAlg
    },
    'otc': {
        'dualema': OtcDualemaAlg,
        'btrader': OtcBestTraderAlg,
        'bbands': OtcBBandsAlg,
        #'rforest': OtcRandForestAlg,
        #'kmeans': OtcKmeansAlg,
        #'kdtree': OtcKdTreeAlg
    }
}

algitems = ['dualema', 'btrader', 'bbands']

@shared_task
def run_algitem(opt, targets, starttime, endtime, base='stock', order=[], stockids=[], traderids=[], limit=10, cfg={}, callback=None, debug=False):
    """ middleware to run as summary info or getting detail info """
    # assert ...

    item = {}

    for target in targets:
        if target in algitems:
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
            alghandler = algdb_tasks[opt][target](**kwargs) 
            alghandler.run()
            if callback == 'insert_summary':
                alghandler.finalize(alghandler.insert_summary)
            elif callback == 'to_detail':
                dt = alghandler.finalize(alghandler.to_detail)
                if dt:
                    item.update({target+'item': dt})
        return item

@shared_task
def collect_algitem(opt, targets, starttime, endtime, base='stock', order=[], stockids=[], traderids=[], limit=10, cfg={}, callback=None, debug=False):
    # assert ...

    item = {}

    for target in targets:
        if target in algitems:
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
            alghandler = algdb_tasks[opt][target](**kwargs) 
            args = (starttime, endtime, cfg, order, limit)
            dt = alghandler.query_summary(*args)
            if dt:
                item.update({target+'item': dt})
    return item

