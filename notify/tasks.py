# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task
from notify.ggmail import GGMail
from notify.gline import GLine

ntyitems = ['gmail', 'line']

@shared_task
def collect_ntyitem(opt, targets, starttime, endtime, base='stock', order=[], stockids=[], traderids=[], limit=10, cfg={}, callback=None, debug=False):

    for target in targets:
        if target in ntyitems:
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
        if target == 'gmail':
            gmail = GGMail(**kwargs)
            msg = gmail.create_msg()
            gmail.send(msg)

        if target == 'line':
            line = GLine(**kwargs)
            msg = line.create_msg()
            line.send(msg)