# -*- coding: utf-8 -*-

import pytz

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

# Import exponential moving average from talib wrapper
from zipline.transforms.ta import EMA

from datetime import datetime, timedelta

from bin.mongodb_driver import *
from query.hisdb_query import *
from query.iddb_query import *
from algorithm.report import Report

class ZombieAlgorithm(TradingAlgorithm):
    """
    This algorithm use strong buy/sell signals following by topbuy/
    topsell info, if topbuy's volume >= stockid.volume * 10 % then buy a count,
    after checking topsell's volume >= stockid.volume * 10 % then sell a count if shared has count
    """

    def __init__(self, dbquery, *args, **kwargs):
        super(ZombieAlgorithm, self).__init__(*args, **kwargs)
        self.dbquery = dbquery
        self.mstockid = self.dbquery.stockmap.keys()[0]

    def initialize(self, ema_window=10):
        # To keep track of whether we invested in the stock or not
        # pool checkpoint
        self.invested = False
        self.idxmin = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.idxmax = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.idxcur = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.idxbuy = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.idxsell = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)

    def handle_data(self, data):
        # minidx
        if self.idxmin[1] == -1:
            self.idxmin = (data[self.mstockid].dt, data[self.mstockid].price, data[self.mstockid].volume)
        else:
            if data[self.mstockid].price <= self.idxmin[1]:
                self.idxmin = (data[self.mstockid].dt, data[self.mstockid].price, data[self.mstockid].volume)

        # maxidx
        if self.idxmax[1] == -1:
            self.idxmax = (data[self.mstockid].dt, data[self.mstockid].price, data[self.mstockid].volume)
        else:
            if data[self.mstockid].price >= self.idxmax[1]:
                self.idxmax = (data[self.mstockid].dt, data[self.mstockid].price, data[self.mstockid].volume)

        # curidx
        self.idxcur = (data[self.mstockid].dt, data[self.mstockid].price, data[self.mstockid].volume)

        self.buy = False
        self.sell = False

        #buyrule
        self.buy = self.idxmax[0] <= self.idxmin[0] - timedelta(days=30) and \
        self.idxcur[0] >= self.idxmin[0] + timedelta(days=1) and \
        self.idxmax[0] <= self.idxcur[0] - timedelta(days=31)

        #sellrule
        if self.invested:
            self.sell = self.idxcur[0] >= self.idxbuy[0] + timedelta(3)

        if self.buy and not self.invested:
            self.order(self.mstockid, 100)
            self.invested = True
            self.buy = True
            self.sell = False
            self.idxbuy = (data[self.mstockid].dt, data[self.mstockid].price)
        elif self.sell and self.invested:
            self.order(self.mstockid, -100)
            self.invested = False
            self.buy = False
            self.sell = True

        # save to recorder
        signals = {
            'open': data[self.mstockid].open,
            'high': data[self.mstockid].high,
            'low': data[self.mstockid].low,
            'close': data[self.mstockid].close,
            'volume': data[self.mstockid].volume,
            'buy': self.buy,
            'sell': self.sell
        }

        # sideband signals
        try:
            signals.update({
                'topbuy0_%s' % (self.dbquery.find_stockmap(self.mstockid, 'topbuy0')): data[self.mstockid].topbuy0,
                'topsell0_%s' % (self.dbquery.find_stockmap(self.mstockid, 'topsell0')): data[self.mstockid].topsell0
            })
        except:
          pass
        self.record(**signals)


if __name__ == '__main__':
    # set time window
    starttime = datetime.utcnow() - timedelta(days=60)
    endtime = datetime.utcnow()
    report = Report(
        algname=ZombieAlgorithm.__name__,
        sort=[('ending_value', 1), ('close', -1)], limit=2)

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
        zombie = ZombieAlgorithm(dbquery=dbquery)
        results = zombie.run(data).dropna()
        report.collect(stockid, results)

    for stockid in report.iter_stockid():
        report.iter_report(stockid, dtype='html')

    stream = report.summary(dtype='html')
    report.write(stream, 'zombie.html')
