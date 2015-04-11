# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task
from celery import chain

from handler.tasks import *

from celery.utils.log import get_task_logger
logger = get_task_logger('algorithm')


@shared_task
def run_algorithm(hisdb, alg, starttime, endtime, stockids, traderids):
    pass
