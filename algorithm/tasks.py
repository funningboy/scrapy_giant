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

@shared_task(time_limit=60*60*60)
def run_algitem(stream):
    args, kwargs = pickle.loads(stream)

    opt = kwargs.get('opt', None)
    targets = kwargs.get('targets', [])
    callback = kwargs.get('callback', None)

    item = {}
    for target in targets:
        if target in algitems:
            alghandler = algdb_tasks[opt][target](**kwargs) 
            alghandler.run()
            if callback == 'insert_summary':
                alghandler.finalize(alghandler.insert_summary)
            elif callback == 'to_detail':
                dt = alghandler.finalize(alghandler.to_detail)
                if dt:
                    item.update({target+'item': dt})
        return pickle.dumps(item)

@shared_task(time_limit=60*60)
def collect_algitem(stream):
    args, kwargs = pickle.loads(stream)

    opt = kwargs.get('opt', None)
    targets = kwargs.get('targets', [])

    starttime = kwargs.get('starttime', None)
    endtime = kwargs.get('endtime', None)
    cfg = kwargs.get('cfg', None)
    constraint = kwargs.get('constraint', None)
    order = kwargs.get('order', None)
    limit = kwargs.get('limit', 10)
    callback = kwargs.get('callback', None)
    debug = kwargs.get('debug', False)
        
    item = {}
    for target in targets:
        if target in algitems:
            alghandler = algdb_tasks[opt][target](**kwargs) 
            args = (starttime, endtime, cfg, constraint, order, limit, callback)
            dt = alghandler.query_summary(*args)
            if dt:
                item.update({target+'item': dt})
    return pickle.dumps(item)

