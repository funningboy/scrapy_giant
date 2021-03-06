# -*- coding: utf-8 -*-
# ref:    http://scikit-learn.org/stable/auto_examples/randomized_search.html

import pytz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import traceback

from datetime import datetime, timedelta
from collections import deque

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV

from bin.mongodb_driver import *
from bin.start import *
from handler.tasks import collect_hisframe
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler

from algorithm.report import Report
from algorithm.register import AlgRegister

class RandForest(TradingAlgorithm):
    """ RandForest
    buy:
    sell:
    """

    def __init__(self, dbhandler, *args, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._cfg = {
            'buf_win': kwargs.pop('buf_win', 15),
            'buy_hold': kwargs.pop('buy_hold', 5),
            'sell_hold': kwargs.pop('sell_hold', 5),
            'buy_amount': kwargs.pop('buy_amount', 1000),
            'sell_amount': kwargs.pop('sell_amount', 1000),        
            'samples': kwargs.pop('samples', 500),
            'trains': kwargs.pop('trains', 100),
            'tests': kwargs.pop('tests', 10),
            'trend_up': kwargs.pop('trend_up', True),
            'trend_down': kwargs.pop('trend_down', True),
            'score': kwargs.pop('score', 0.99)
        }
        super(RandForest, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids

    @property
    def cfg(self):
        return self._cfg

    def initialize(self):
        self.clf = RandomForestClassifier(n_estimators=20)
        self.window = deque(maxlen=self._cfg['buf_win'])
        self.X = deque(maxlen=self._cfg['samples'])
        self.Y = deque(maxlen=self._cfg['samples'])
        self.trained = False
        self.tested = False
        self.match = False
        self.invested_buy = False
        self.invested_sell = False
        self.buy = False
        self.sell = False
        self.buy_hold = 0
        self.sell_hold = 0
 
    def handle_data(self, data):
        sid = self.sids[0]
        self.window.append((
            data[sid].open,
            data[sid].high,
            data[sid].low,
            data[sid].close,
            data[sid].volume
        ))

        if len(self.window) == self._cfg['buf_win']:
            open, high, low, close, volume = [np.array(i) for i in zip(*self.window)]
            changes = np.diff(close) / close[1:]

            # as train & target seqs
            # ex up(1): [0, 0 , 0, ...1, 1], down(0): [1, 1, 1, .. 0, 0]
            self.X.append(changes[:-1])
            self.Y.append(changes[-1] > 0)

            # train
            if not self.trained and not self.tested:
                if len(self.Y) == self._cfg['trains'] and len(self.X) == self._cfg['trains']:
                    X, y = np.array(list(self.X)), np.array(list(self.Y))
                    self.clf.fit(X, y)
                    self.X.clear()
                    self.Y.clear()
                    self.trained = True

            # test
            if self.trained and not self.tested:    
                if len(self.Y) == self._cfg['tests'] and len(self.Y) == self._cfg['tests']:
                    X, y = np.array(list(self.X)), np.array(list(self.Y))
                    score = self.clf.score(X, y).mean()
                    print "predict score mean %.2f" %(score)
                    if score > self._cfg['score']:
                        self.match = True
                    self.tested = True

            if self.match:
                for i, change in enumerate(changes):

                    self.buy_hold = self.buy_hold - 1 if self.buy_hold > 0 else self.buy_hold
                    self.sell_hold = self.sell_hold - 1 if self.sell_hold > 0 else self.sell_hold
                    self.buy = False
                    self.sell = False

                    # sell after buy
                    if self._cfg['trend_up']:
                        if change > 0 and not self.invested_buy:
                            self.order(sid, self._cfg['buy_amount'])
                            self.invested_buy = True
                            self.buy = True
                            self.buy_hold = self._cfg['buy_hold']
                        elif self.invested_buy == True and self.buy_hold == 0:
                            self.order(sid, -self._cfg['buy_amount'])
                            self.invested_buy = False
                            self.sell = True

                    # buy after sell
                    if self._cfg['trend_down']:
                        if change < 0 and not self.invested_sell:
                            self.order(sid, -self._sell_cfg['amount'])
                            self.invested_sell = True
                            self.sell = True
                            self.sell_hold = self._cfg['sell_hold']
                        elif self.invested_sell == True  and self.sell_hold == 0:
                            self.order(sid, self._cfg['sell_amount'])
                            self.invested_sell = False
                            self.buy = True

 
                    # save to recorder
                    signals = {
                        'open': open[i],
                        'high': high[i],
                        'low': low[i],
                        'close': close[i],
                        'volume': volume[i],
                        'buy': self.buy,
                        'sell': self.sell
                    }
                    self.record(**signals)
                return

# register to alg tasks
AlgRegister.add(RandForest)

def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    maxlen = 30
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    report = Report(
        'randforest', 
        sort=[('buys', False), ('sells', False), ('portfolio_value', False)], limit=20)

    kwargs = {
        'debug': debug,
        'limit': limit,
        'opt': opt
    }
    # fetch
    idhandler = TwseIdDBHandler(**kwargs) if kwargs['opt'] == 'twse' else OtcIdDBHandler(**kwargs)
    for stockid in idhandler.stock.get_ids():
        try:
            kwargs = {
                'opt': opt,
                'targets': ['stock', 'future', 'credit'],
                'starttime': starttime,
                'endtime': endtime,
                'stockids': [stockid],
                'traderids': [],
                'base': 'stock',
                'order': [],
                'callback': None,
                'limit': 1,
                'debug': debug
            }
            panel, dbhandler = collect_hisframe(**kwargs)
            if len(panel[stockid].index) < maxlen:
                continue
            rforest = RandForest(dbhandler=dbhandler)
            results = rforest.run(panel).fillna(0)
            risks = rforest.perf_tracker.handle_simulation_end()
            report.collect(stockid, results, risks)
            print "%s pass" %(stockid)
        except:
            print traceback.format_exc()
            continue

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'randforest.html')

    for stockid in report.iter_symbol():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "randforest_%s.html" % (stockid))

    # plot
    for stockid in report.iter_symbol():
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
    parser = argparse.ArgumentParser(description='test RandForest algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store', type=str, default='twse', help='twse/otc')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    #proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    #close_main_service(proc, args.debug)
