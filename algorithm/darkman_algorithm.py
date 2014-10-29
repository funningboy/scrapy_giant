# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

class DarkManAlgorithm(TradingAlgorithm):
    """
    """

    def __init__(self, dbquery, *args, **kwargs):
        super(DarkManAlgorithm, self).__init__(*args, **kwargs)
        self.dbquery = dbquery
        self.mstockid = self.dbquery._stockmap.keys()[0]

    def initialize(self):
        pass

if __name__ == '__main__':
    # set time window
    starttime = datetime.utcnow() - timedelta(days=60)
    endtime = datetime.utcnow()
    report = Report(
        algname=DarkManAlgorithm.__name__,
        sort=[('ending_value', 1), ('close', -1)], limit=20)

    # set debug or normal mode
    kwargs = {
        'debug': False,
        'limit': 0
    }
    for stockid in TwseIdDBQuery().get_stockids(**kwargs):
        dbquery = TwseHisDBQuery()
        data = dbquery.get_all_data(
            starttime=starttime, endtime=endtime,
            stockids=[stockid], traderids=[])
        if data.empty:
            continue
        darkman = DarkManAlgorithm(dbquery=dbquery)
        results = darkman.run(data).dropna()
        report.collect(stockid, results)

    for stockid in report.iter_stockid():
        report.iter_report(stockid, dtype='html')

    stream = report.summary(dtype='html')
    report.write(stream, 'darkman.html')

