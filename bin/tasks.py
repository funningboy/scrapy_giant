# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pickle
import subprocess
from bin.start import wap_scrapy_cmd
from giant.celery import app
from celery import shared_task
from bin.adsl import *

from celery.utils.log import get_task_logger
logger = get_task_logger('bin')

# scrapy tasks sync
scrapy_tasks = [
# id
    'twseid',
    'otcid',
    'traderid',
# twse
    'twsehistrader',
    'twsehistrader2',
    'twsehisstock',
    'twsehiscredit',
    'twsehisnocredit',
# otc
    'otchistrader',
    'otchistrader2',
    'otchisstock',
    'otchiscredit',
    'otchisnocredit'
]

@app.task
def nsum(stream):
    import time
    import random
    args, kwargs = pickle.loads(stream)
    time.sleep(random.randint(0, 1))
    r = sum(args)
    print "test celey nsum %d" %(r)
    return pickle.dumps(r)

@shared_task
def navg(stream):
    import time
    import random
    args, kwargs = pickle.loads(stream)
    time.sleep(random.randint(5, 10))
    r = sum(args)/len(args) if len(args) != 0 else 0
    print "test celey navg %d" %(r)
    return pickle.dumps(r)

@shared_task
def run_scrapy_service(spider, loglevel, logfile, logen=True, debug=False):
    cmd = wap_scrapy_cmd(
        spider=spider,
        loglevel=loglevel,
        logfile=logfile,
        logen=logen,
        debug=debug)
    proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.communicate()

@shared_task
def run_adsl_service():
    reset_adsl()