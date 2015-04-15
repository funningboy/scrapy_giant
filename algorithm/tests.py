# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

import timeit
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from bin.tests import *
from handler.tasks import *
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.models import StockMapColl, TraderMapColl

from django.template import Context, Template

class TestTwseDualemaAlg(TestTwseHisTrader2, TestTwseHisStock):

    def test_on_run(self, opt='twse', alg='dualema'):
        super(TestTwseDualemaAlg, self).test_on_run()
        args = (opt, alg, starttime, endtime, 10, True)
        alg = run_algorithm_service.delay(*args).get()
        algitem = alg.query_summary()
        for it in algitem:
            print it.end_time, it.portfolio_value
        
        alg = algdb_tasks[opt][alg]()
        args = (starttime, endtime, ['2317'], [], 'totalvolume', 10, alg.to_detail)
        alg.run(*args)
        algitem = alg.query_detail()
        for it in algitem:
            print it.time, it.open, it.portfolio_value

class TestTwseBestTraderAlg():

    def test_on_run(self, opt='twse', alg='btrader'):
        super(TestTwseBestTraderAlg, self).test_on_run()
        algs = (opt, alg, starttime, endtime, 10, True)
        alg = run_algorithm_service.delay(*args).get()
        algitem = alg.query_summary()
        for it in algitem:
            print it.end_time, it.portfolio_value

        args = (starttime, endtime, ['2317', '2330', '1314'], ['1440'], 'totalvolume', 10, alg.to_detail)
        alg.run(*args)
        algitem = alg.query_detail()
        for it in algitem:
            print it.time, it.open, it.portfolio_value


