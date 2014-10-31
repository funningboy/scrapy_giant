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

@celery.task(name='bin.tasks.run_algorithm')
def run_algorithm(starttime, endtime, stockids=[], traderids=[], debug=False):
    dbquery = TwseHisDBQuery()
    data = dbquery.get_all_data(
        starttime=starttime, endtime=endtime,
        stockids=stockids, traderids=traderids)
    if data.empty:
        return
    dualema = DualEMATaLib(dbquery=dbquery)
    results = dualema.run(data).dropna()

    #superman = SuperMa

