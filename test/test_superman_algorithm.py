# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from algorithm.superman.superman_algorithm import SuperManAlgorithm

from test.test_start import *
from query.iddb_query import *
from query.hisdb_query import *
from algorithm.report import Report

class TestSuperManAlgorithm(TestTwseHisAll):

    def test_on_run(self):
        # set time window
        starttime = datetime.utcnow() - timedelta(days=60)
        endtime = datetime.utcnow()
        report = Report(
            algname=SuperManAlgorithm.__name__,
            sort=[('ending_value', 1), ('close', -1)], limit=20)

        # set debug or normal mode
        kwargs = {
            'debug': True,
            'limit': 0
        }
        for stockid in TwseIdDBQuery().get_stockids(**kwargs):
            twsedbquery = TwseHisDBQuery()
            data = twsedbquery.get_all_data(
                starttime=starttime, endtime=endtime,
                stockids=[stockid], traderids=[])
            if data.empty:
                continue

            supman = SuperManAlgorithm(dbquery=twsedbquery)
            results = supman.run(data).dropna()
            report.collect(stockid, results)

        for stockid in report.iter_stockid():
            report.iter_report(stockid, dtype='html')

        stream = report.summary(dtype='html')
        report.write(stream, 'superman.html')
