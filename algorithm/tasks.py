# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task
from celery import chain

from handler.tasks import *
from algorithm.report import Report
from algorithm.dualema_algorithm import DualEMAAlgorithm

from celery.utils.log import get_task_logger
logger = get_task_logger('algorithm')

# alg tasks sync
alg_tasks = {
    'dualema': DualEMAAlgorithm
}

