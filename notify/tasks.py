# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
import pickle
from celery import shared_task
from notify.ggmail import GGMail
from notify.gline import GLine

ntyitems = ['gmail', 'line']

@shared_task(time_limit=60)
def collect_ntyitem(stream):
    args, kwargs = pickle.loads(stream)

    for target in targets:
        if target == 'gmail':
            gmail = GGMail(**kwargs)
            msg = gmail.create_msg()
            gmail.send(msg)

        if target == 'line':
            line = GLine(**kwargs)
            msg = line.create_msg()
            line.send(msg)