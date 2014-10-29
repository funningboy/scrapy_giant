# -*- coding: utf-8 -*-

import time
import pandas as pd
import os

from celery import Celery

from bin.mongodb_driver import *
from query.hisdb_query import *
from query.iddb_query import *
from algorithm.report import Report
from algorithm.dualema.dualema_algorithm import DualEMATaLib

_rootpath = os.environ.get('ROOTPATH', './tmp')
_dbpath = os.environ.get('DBPATH', _rootpath)
_logpath = os.environ.get('LOGPATH', _rootpath)
_host = os.environ.get('HOSTNAME', 'localhost')
_port = int(os.environ.get('DBPORT', '27017'))
_mongod = os.environ.get('MONGOD', 'mongod')

#
#Specify mongodb host and datababse to connect to
BROKER_URL = 'mongodb://%(host)s:%(port)s/%(db)s' % {
    'host': _host,
    'port': _port,
    'db': _rootpath
}

celery = Celery('algorithm', broker=BROKER_URL)

#Loads settings for Backend to store results of jobs
celery.config_from_object('algorithm.celeryconfig')

@celery.task(name='bin.tasks.run_algorithm')
def run_dualema(starttime, endtime, stockids=[], traderids=[], debug=False):
    dbquery = TwseHisDBQuery()
    data = dbquery.get_all_data(
        starttime=starttime, endtime=endtime,
        stockids=stockids, traderids=traderids)
    if data.empty:
        return
    dualema = DualEMATaLib(dbquery=dbquery)
    results = dualema.run(data).dropna()


