# -*- coding: utf-8 -*-

# as event
from main.table import default_tags

def hisstock_list_tags(**kwargs):
    return default_tags(**kwargs)

def hisstock_detail_tags(**kwargs):
    tags = default_tags(**kwargs)
    tags.update({
        'starttime': kwargs.pop('starttime', None),
        'endtime': kwargs.pop('endtime', None),
        'stockids': kwargs.pop('stockids', []),
        'traderids': kwargs.pop('traderids', []),
        'opt': kwargs.pop('opt', None),
        'algorithm': kwargs.pop('algorithm', None),
        'debug': kwargs.pop('debug', False)
    })
    return tags

def histrader_list_tags(**kwargs):
    tags = default_tags(**kwargs)
    tags.update({
        'starttime': kwargs.pop('starttime', None),
        'endtime': kwargs.pop('endtime', None),
        'opt': kwargs.pop('opt', None),
        'algorithm': kwargs.pop('algorithm', None),
        'debug': kwargs.pop('debug', False)
    })
    return tags

def histrader_detail_tags(**kwargs):
    return default_tags(**kwargs)

def default_hiscollect(**kwargs):
    starttime = kwargs.pop('starttime', None)
    endtime = kwargs.pop('endtime', None)
    stockids =  kwargs.pop('stockids', [])
    traderids = kwargs.pop('traderids', [])
    opt = kwargs.pop('opt', None)
    algorithm = kwargs.pop('algorithm', None)
    debug = kwargs.pop('debug', False)

    collect = {
        'starttime': starttime,
        'endtime': endtime,
        'stockids': stockids,
        'traderids': traderids,
        'algorithm': algorithm,
        'opt': opt,
        'type': None,
        'debug': debug,
        'frame': {
            'hisstock': {
                'on': False,
                'starttime': starttime,
                'endtime': endtime,
                'stockids': stockids,
                'base': 'stock',
                'order': ['-totalvolume', '-totaldiff'],
                'callback': None,
                'limit': 10,
                'priority': 0
            },
            'hiscredit': {
                'on': False,
                'starttime': starttime,
                'endtime': endtime,
                'stockids': stockids,
                'base': 'stock',
                'order': ['-financeused', '-bearishused'],
                'callback': None,
                'limit': 10,
                'priority': 1
            },
            'histrader': {
                'on': False,
                'starttime': starttime,
                'endtime': endtime,
                'stockids': stockids,
                'traderids': traderids,
                'base': 'stock',
                'order': ['-totalvolume'],
                'callback': None,
                'limit': 10,
                'priority': 3,
            },
            'hisfuture': {
                'on': False,
                'starttime': starttime,
                'endtime': endtime,
                'stockids': stockids,
                'base': 'stock',
                'order': ['-totaldiff'],
                'callback': None,
                'limit': 10,
                'priority': 2
            }
        }
    }
    return collect
