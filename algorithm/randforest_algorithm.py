# -*- coding: utf-8 -*-

import pytz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import traceback

from datetime import datetime, timedelta
from collections import deque

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *
from zipline.transforms.ta import EMA
from zipline.transforms.stddev import MovingStandardDev
from zipline.transforms.mavg import MovingAverage

from scipy.stats import randint as sp_randint
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from algorithm.report import Report


class RandForestAlgorithm(TradingAlgorithm):
    """
    http://scikit-learn.org/stable/auto_examples/randomized_search.html
    """

    def __init__(self, dbhandler, *args, **kwargs):
        self.n_estimators = kwargs.pop('n_estimators', 20)
        self.maxlen = kwargs.pop('maxlen', 70)
        super(RandForestAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids

    def initialize(self):
        self.clf = RandomForestClassifier(n_estimators=self.n_estimators)
        self.window = deque(maxlen=self.maxlen)
        self.X = deque(maxlen=self.maxlen*2)
        self.Y = deque(maxlen=self.maxlen*2)
        self.add_transform(MovingAverage, 'mavg', ['price', 'volume'], window_length=7)
        self.add_transform(MovingStandardDev, 'stddev', window_length=7)

    def handle_data(self, data):
        self.window.append(data[self.sids[0]].price)

        if len(self.window) == self.maxlen:
            changes = np.diff(self.window) > 0

            # as train & target seqs
            # ex up(1): [0, 0 , 0, ...1, 1], down(0): [1, 1, 1, .. 0, 0]
            self.X.append(changes[:-1])
            self.Y.append(changes[-1])

            if len(self.Y) >= self.maxlen*2//3:
                self.clf.fit(self.X, self.Y)
                self.prediction = self.clf.predict(changes[1:])
                self.order_target_percent(self.sids[0], self.prediction)
                # save to recorder
                signals = {
                    'open': data[self.sids[0]].open,
                    'high': data[self.sids[0]].high,
                    'low': data[self.sids[0]].low,
                    'close': data[self.sids[0]].close,
                    'volume': data[self.sids[0]].volume,
                    'mavg7': data[self.sids[0]].mavg.price,
                    'prediction': self.prediction
                }
                self.record(**signals)


class RandForestAlgorithm2(TradingAlgorithm):
    """
    label samples : -2:(T(-1)>=1.03*T(0)), -1:(T(-1)<1.03*T(0)&&T(-1)>T(0)), 0:(T(-1)==T(0)), 1, 2
    features : 1:T(1)>T(0) 0:T(1)=T(0) -1:
    """

    def __init__(self, dbhandler, *args, **kwargs):
        self.n_estimators = kwargs.pop('n_estimators', 20)
        self.maxlen = kwargs.pop('maxlen', 70)
        super(RandForestAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids

    def initialize(self):
        self.clf = RandomForestClassifier(n_estimators=self.n_estimators)
        self.window = deque(maxlen=self.maxlen)
        self.X = deque(maxlen=self.maxlen*2)
        self.Y = deque(maxlen=self.maxlen*2)
        self.add_transform(MovingAverage, 'mavg', ['price', 'volume'], window_length=7)
        self.add_transform(MovingStandardDev, 'stddev', window_length=7)

    def _enocde(self, pre, cur):
         ratio = pre.close/cur.close
         if ratio >= 1.03: return -2
         elif ratio < 1.03 and ratio >= 1.01: return -1
         elif ratio <= 0.99 and ratio > 0.97: return 1
         elif ratio < 0.97: return 2
         else: return 0

    def handle_data(self, data):
        self.window.append(data[self.sids[0]].price)

        if len(self.window) == self.maxlen:
            # as train & target seqs
            # ex up(1,2): [0, 0 , 0, ...1, 1], down(0,-1): [1, 1, 1, .. 0, 0]
            self.X.append([self._encode(self.window[i], self.window[i+1]) for i in range(0, self.maxlen-3)])
            self.Y.append([self._encode(self.window[i], self.window[i+1]) for i in range(self.maxlen-3, -1)])

            if len(self.Y) >= self.maxlen*2//3:
                self.clf.fit(self.X, self.Y)
                self.prediction = self.clf.predict(changes[1:])
                self.order_target_percent(self.sids[0], self.prediction)
                # save to recorder
                signals = {
                    'open': data[self.sids[0]].open,
                    'high': data[self.sids[0]].high,
                    'low': data[self.sids[0]].low,
                    'close': data[self.sids[0]].close,
                    'volume': data[self.sids[0]].volume,
                    'mavg7': data[self.sids[0]].mavg.price,
                    'prediction': self.prediction
                }
                self.record(**signals)


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    # set time window
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    # sort factor
    report = Report(
        sort=[('buy_count', False), ('sell_count', False), ('volume', False)], limit=20)
    # set debug or normal mode
    kwargs = {
        'debug': debug,
        'limit': limit,
        'opt': opt
    }
    idhandler = TwseIdDBHandler() if kwargs['opt'] == 'twse' else OtcIdDBHandler()
    for stockid in idhandler.stock.get_ids(**kwargs):
        try:
            dbhandler = TwseHisDBHandler() if kwargs['opt'] == 'twse' else OtcHisDBHandler()
            dbhandler.stock.ids = [stockid]
            data = dbhandler.transform_all_data(starttime, endtime, [stockid], [], 'totalvolume', 10)
            supman = RandForestAlgorithm(dbhandler=dbhandler)
            results = supman.run(data).fillna(0)
            report.collect(stockid, results)
            print "%s pass" %(stockid)
        except:
            print traceback.format_exc()
            continue

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'randforest.html')

    for stockid in report.iter_stockid():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "randforest_%s.html" % (stockid))

    # plot
    for stockid in report.iter_stockid():
        try:
            perf = report.pool[stockid]
            fig = plt.figure()
            ax1 = fig.add_subplot(211)
            perf.portfolio_value.plot(ax=ax1)
            ax1.set_ylabel('portfolio value in $')

            ax2 = fig.add_subplot(212)
            perf[['close', 'mavg7']].plot(ax=ax2)

            perf_trans = perf.ix[[t != [] for t in perf.transactions]]
            buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
            sells = perf_trans.ix[[t[0]['amount'] < 0 for t in perf_trans.transactions]]
            ax2.plot(buys.index, perf.close.ix[buys.index],
                     '^', markersize=10, color='m')
            ax2.plot(sells.index, perf.close.ix[sells.index],
                     'v', markersize=10, color='k')
            ax2.set_ylabel('price in $')
            plt.legend(loc=0)
            plt.savefig("randforest_%s.png" %(stockid))
            #plt.show()
        except:
            continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test randforest algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store', type=str, default='twse', help='twse/otc')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    close_main_service(proc, args.debug)
