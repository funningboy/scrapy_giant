# -*- coding: utf-8 -*-
from __future__ import absolute_import

#from main.celery import app
from celery import shared_task
from celery import chain

from handler.tasks import *
from algorithm.report import Report
from algorithm.dualema_algorithm import DualEMATaLib
from algorithm.superman_algorithm import SuperManAlgorithm
from algorithm.darkman_algorithm import DarkManAlgorithm
from algorithm.zombie_algorithm import ZombieAlgorithm

from celery.utils.log import get_task_logger
logger = get_task_logger('algorithm')

# alg tasks sync
alg_tasks = {
    'superman': SuperManAlgorithm,
    'darkman': DarkManAlgorithm,
    'zombie': ZombieAlgorithm,
    'dualema': DualEMATaLib
}

# as alg service
@shared_task
def run_algorithm_service(data, ):

    chain(
            (source_file),         # Fetch data from remote source
                                tasks.blacklist.s(),                # Remove blacklisted records
                                tasks.transform.s(),                # Transform raw data ready for loading
                                tasks.load.s(),                     # Load into DB
                            ).apply_async()
