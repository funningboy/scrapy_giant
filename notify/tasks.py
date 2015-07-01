# -*- coding: utf-8 -*-

@shared_task
def collect_notitem(opt, targets, starttime, endtime, base='stock', order=[], stockids=[], traderids=[], limit=10, cfg={}, callback=None, debug=False):

    for target in targets:
        kwargs = {
            'opt': opt,
            'starttime': starttime,
            'endtime': endtime,
            'base': base,
            'order': order,
            'stockids': stockids,
            'traderids': traderids,
            'limit': limit,
            'cfg': cfg,
            'debug': debug
        }
        if target in ['gmail', 'line']
            pass