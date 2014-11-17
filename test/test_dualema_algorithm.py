# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from algorithm.dualema_algorithm import DualEMATaLib

from test.test_start import TestTwseHisAll
from query.iddb_query import *
from query.hisdb_query import *
from algorithm.report import Report

class TestDualEMATaLib(TestTwseHisAll):

    def test_on_run(self):
        # set time window
        starttime = datetime.utcnow() - timedelta(days=60)
        endtime = datetime.utcnow()
        report = Report(
            algname=DualEMATaLib.__name__,
            sort=[('ending_value', False), ('close', False)], limit=20)

        # set debug or normal mode
        kwargs = {
            'debug': True,
            'limit': 0
        }
        for stockid in TwseIdDBQuery().get_stockids(**kwargs):
            dbquery = TwseHisDBQuery()
            data = dbquery.transform_all_data(
                starttime=starttime, endtime=endtime,
                stockids=[stockid], traderids=[])
            if data.empty:
                continue
            dualema = DualEMATaLib(dbquery=dbquery)
            results = dualema.run(data).dropna()
            if results.empty:
                continue
            report.collect(stockid, results)

        stream = report.summary(dtype='html')
        report.write(stream, 'dualema.html')

        for stockid in report.iter_stockid():
            report.iter_report(stockid, dtype='html')

    # plot
    #import matplotlib.pyplot as plt
    #    # plot results
    #    fig = plt.figure()
    #    ax1 = fig.add_subplot(211, ylabel='portfolio value')
    #    results.portfolio_value.plot(ax=ax1)
    #
    #    ax2 = fig.add_subplot(212)
    #    results[['price', 'short_ema', 'long_ema']].plot(ax=ax2)
    #
    #    ax2.plot(results.ix[results.buy].index, results.short_ema[results.buy],
    #             '^', markersize=10, color='m')
    #    ax2.plot(results.ix[results.sell].index, results.short_ema[results.sell],
    #             'v', markersize=10, color='k')
    #    plt.legend(loc=0)
    #    plt.gcf().set_size_inches(18, 8)

if __name__ == '__main__':
    unittest.main()

