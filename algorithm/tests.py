# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

import timeit
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from algorithm.tasks import *
from django.template import Context, Template

class TestTwseDualemaAlg():

    def test_on_run(self, opt='twse', alg='dualema'):
        super(TestTwseDualemaAlg, self).test_on_run()
        starttime = datetime.utcnow() - timedelta(days=150)
        endtime = datetime.utcnow()
        args = (opt, alg, starttime, endtime, 10, True)
        # as background algorithm service
        run_algorithm_service.delay(*args).get()
        # query summary
        alghandler = algdb_tasks[opt][alg]()
        algitem = alghandler.query_summary()
        self.assertTrue(len(algitem)>0)
        self.assertTrue(algitem[-1].portfolio_value>0)
        # as run/query detail
        alghandler = algdb_tasks[opt][alg]()
        args = (starttime, endtime, ['2317'], [], 'totalvolume', 10, alghandler.to_detail)
        alghandler.run(*args)
        algitem = alghandler.query_detail()
        self.assertTrue(len(algitem)>0)
        self.assertTrue(algitem[-1].open>0)

class TestTwseBestTraderAlg():

    def test_on_run(self, opt='twse', alg='btrader'):
        super(TestTwseBestTraderAlg, self).test_on_run()
        starttime = datetime.utcnow() - timedelta(days=10)
        endtime = datetime.utcnow()
        args = (opt, alg, starttime, endtime, 10, True)
        # as background algorithm service
        run_algorithm_service.delay(*args).get()
        # as run/query summary
        alghandler = algdb_tasks[opt][alg]()
        algitem = alghandler.query_summary()
        self.assertTrue(len(algitem)>0)
        self.assertTrue(algitem[-1].portfolio_value>0)
        # as run/query detail
        # find traders as tops
        args = ('twse', starttime, endtime, ['2317'], [], 'stock', 'totalvolume', 10)
        panel, dbhandler = trans_histoptrader(*args)
        tops = dbhandler.trader.map_alias(['2317'], 'stock', ["top%d" %i for i in range(10)])
        alghandler = algdb_tasks[opt][alg]()
        args = (starttime, endtime, ['2317'], [tops[0]], 'totalvolume', 10, alghandler.to_detail)
        alghandler.run(*args)
        algitem = alghandler.query_detail()
        self.assertTrue(len(algitem)>0)
        self.assertTrue(algitem[-1].open>0)
