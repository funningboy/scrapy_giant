# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import subprocess
import json

from celery import Celery

from bin.mongodb_driver import *
from bin.start import *
from bin.logger import Logger
from query.hisdb_query import (TwseHisDBQuery, OtcHisDBQuery)
from query.iddb_query import (TwseIdDBQuery, OtcIdDBQuery)
from algorithm.report import Report
from algorithm.dualema_algorithm import DualEMATaLib
from algorithm.superman_algorithm import SuperManAlgorithm
from algorithm.zombie_algorithm import ZombieAlgorithm

_rootpath = os.environ.get('ROOTPATH', './tmp')
_dbpath = os.environ.get('DBPATH', _rootpath)
_logpath = os.environ.get('LOGPATH', _rootpath)
_host = os.environ.get('HOSTNAME', 'localhost')
_port = int(os.environ.get('DBPORT', '27017'))
_mongod = os.environ.get('MONGOD', 'mongod')
_debug = os.environ.get('DEBUG', False)

# Specify mongodb host and datababse to connect to
BROKER_URL = 'mongodb://%(host)s:%(port)s/%(db)s' % {
    'host': _host,
    'port': _port,
    'db': _dbpath
}

celery = Celery('bin', broker=BROKER_URL)

# Loads settings for Backend to store results of jobs
celery.config_from_object('bin.celeryconfig')

scrapy_tasks = [
    'twseid',
    'otcid',
    'twsehistrader',
    'twsehisstock',
    'otchistrader',
    'otchisstock'
]

hisdb_tasks = {
    'twse': TwseHisDBQuery,
    'otc': OtcHisDBQuery
}

alg_tasks = {
    'superman': SuperManAlgorithm,
    'zombie': ZombieAlgorithm,
    'dualema': DualEMATaLib
}

# as background service
@celery.task(name='bin.tasks.run_scrapy_service')
def run_scrapy_service(spider, loglevel, logfile, logen=True, debug=False):
    if spider not in scrapy_tasks:
        Logger.error("%s spider not support" % (spider))
        raise Exception
    cmd = wap_scrapy_cmd(
        spider=spider,
        loglevel=loglevel,
        logfile=logfile,
        logen=logen,
        debug=debug
    )
    proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.communicate()

# as background service
@celery.task(name='bin.tasks.run_algorithm_service')
def run_algorithm_service(hisdb, alg, starttime, endtime, stockids=[], traderids=[], debug=False):
    if hisdb not in hisdb_tasks:
        Logger.error("%s hisdb not support" % (hisdb))
        raise Exception
    if alg not in alg_tasks:
        Logger.error("%s algoritm not support" % (alg))
        raise Exception
    dbquery = hisdb_tasks[hisdb]()
    data = dbquery.transform_all_data(
        starttime=starttime,
        endtime=endtime,
        stockids=stockids,
        traderids=traderids
    )
    alg = alg_tasks[alg](dbquery)
    results = alg.run(data).dropna()
    return results

