# -*- coding: utf-8 -*-
from __future__ import absolute_import

import subprocess
from bin.start import wap_scrapy_cmd
from giant.celery import app
from celery import shared_task

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
def add(x, y):
    import time
    import random
    time.sleep(random.randint(0, 1))
    r = x + y
    print "test celey add %d" %(r)
    return r

@shared_task
def mux(x, y):
    import time
    import random
    time.sleep(random.randint(5, 10))
    r = x * y
    print "test celey mux %d" %(r)
    return r

# as background service
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
