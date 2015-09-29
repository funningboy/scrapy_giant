# -*- coding: utf-8 -*-
# ref: http://scikit-learn.org/stable/auto_examples/applications/plot_stock_market.html
# https://www.quantopian.com/posts/working-with-history-dataframes

import pandas as pd
import numpy as np
import pytz
import matplotlib.pyplot as plt
import traceback

from matplotlib.collections import LineCollection
from sklearn import cluster, covariance, manifold

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *
from zipline.finance.execution import LimitOrder
from zipline.finance.trading import SimulationParameters

from datetime import datetime, timedelta
from collections import deque

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.tasks import collect_hisframe

from algorithm.report import Report


class BestTraderAlgorithm(TradingAlgorithm):
    """ find the best correlation between trader and stocks
    buy:
    sell:
    """

    def __init__(self, dbhandler, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._buf_win = kwargs.pop('buf_win', 2)
        self._buy_hold = kwargs.pop('buy_hold', 3)
        self._sell_hold = kwargs.pop('sell_hold', 3)
        self._buy_amount = kwargs.pop('buy_amount', 1000)
        self._sell_amount = kwargs.pop('sell_amount', 1000)
        self._trend_up = kwargs.pop('trend_up', True)
        self._trend_down = kwargs.pop('trend_down', True)
        super(BestTraderAlgorithm, self).__init__(**kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids
        self.tids = self.dbhandler.trader.ids
        self.tops = list(self.dbhandler.trader.get_alias([self.sids[0]], 'trader', ["top%d" %i for i in range(10)]))
        self.tops = {k:v for v,k in enumerate(self.tops)}
        if self._debug:
            print self.tops

    def initialize(self):
        self.window = deque(maxlen=self._buf_win)
        self.invested_buy = False
        self.invested_sell = False
        self.buy = False
        self.sell = False
        self.buy_hold = 0
        self.sell_hold = 0

    def handle_data(self, data):
        sid, toptid, tid = self.sids[0], self.tops[self.tids[0]], self.tids[0]
        date = data[sid].datetime

        try:
            self.window.append((
                getattr(data[sid], "top%d_buyvolume" %(toptid)),
                getattr(data[sid], "top%d_sellvolume" %(toptid)),
                getattr(data[sid], "top%d_avgbuyprice" %(toptid)),
                getattr(data[sid], "top%d_avgsellprice" %(toptid)),
                getattr(data[sid], "top%d_ratio" %(toptid)),
                data[sid].open,
                data[sid].high,
                data[sid].low,
                data[sid].close,
                data[sid].volume
            ))
        except:
            if self._debug:
                print "%s: traderid(%s) not found in stockid(%s)" %(date, tid, sid)
            pass    

        if len(self.window) == self._buf_win:
            buyvolume, sellvolume, avgbuyprice, avgsellprice, ratio, open, high, low, close, volume = [np.array(i) for i in zip(*self.window)]
 
            self.buy = False
            self.sell = False

            if buyvolume[-1]:
                self.order_target_percent(sid, buyvolume[-1], style=LimitOrder(avgbuyprice[-1]))
                self.buy = True
            if sellvolume[-1]:
                self.order_target_percent(sid, -sellvolume[-1], style=LimitOrder(avgsellprice[-1]))
                self.sell = True

            sideband = {
                "top%d_%s_buyvolume" % (toptid, tid): buyvolume[-1],
                "top%d_%s_sellvolume" % (toptid, tid): sellvolume[-1],
                "top%d_%s_avgbuyprice" % (toptid, tid): avgbuyprice[-1],
                "top%d_%s_avgsellprice" % (toptid, tid): avgsellprice[-1]
            }
  
            # save to recorder
            signals = {
                'open': open[-1],
                'high': high[-1],
                'low':  low[-1],
                'close': close[-1],
                'volume': volume[-1],
                'buy': self.buy,
                'sell': self.sell,
            }

            signals.update(sideband)
            self.record(**signals)


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    maxlen = 5
    starttime = datetime.utcnow() - timedelta(days=15)
    endtime = datetime.utcnow()
    report = Report(
        sort=[('buys', False), ('sells', False), ('portfolio_value', False)], limit=20)

    kwargs = {
        'debug': debug,
        'limit': limit,
        'opt': opt
    }
    # 1590:u'花旗環球', 1440:u'美林'
    traderid = '1440'
    idhandler = TwseIdDBHandler(**kwargs) if kwargs['opt'] == 'twse' else OtcIdDBHandler(**kwargs)
    for stockid in idhandler.stock.get_ids():
        try:
            # pre find traderid as top0
            kwargs = {
                'opt': opt,
                'targets': ['trader'],
                'starttime': starttime,
                'endtime': endtime,
                'stockids': [stockid],
                'traderids': [],
                'base': 'stock',
                'constraint': lambda x: x.value["ebuyratio"] > 10 or x.value["totalkeepbuy"] >= 1,
                'order': lambda x: [-x.value["totalvolume"], -x.value["totalbuyratio"]],
                'callback': None,
                'limit': 10,
                'debug': debug
            }
            panel, dbhandler = collect_hisframe(**kwargs)
            tops = list(dbhandler.trader.get_alias([stockid], 'trader', ["top%d" %i for i in range(10)]))
            if not tops:
                continue
                
            print "%s prefound:%s" %(stockid, tops)
            traderid = tops[0] if traderid not in tops else traderid
            # run
            kwargs = {
                'opt': opt,
                'targets': ['stock', 'trader', 'future', 'credit'],
                'starttime': starttime,
                'endtime': endtime,
                'stockids': [stockid],
                'traderids': [traderid],
                'base': 'trader',
                'callback': None,
                'limit': 10,
                'debug': debug
            }
            panel, dbhandler = collect_hisframe(**kwargs)
            if len(panel[stockid].index) < maxlen:
                continue

            sim_params = SimulationParameters(
                period_start=panel[stockid].index[0],
                period_end=panel[stockid].index[-1],
                data_frequency='daily',
                emission_rate='daily'
            )

            besttrader = BestTraderAlgorithm(dbhandler=dbhandler, debug=debug, sim_params=sim_params)
            results = besttrader.run(panel).fillna(0)
            risks = besttrader.perf_tracker.handle_simulation_end()  
            report.collect(stockid, results, risks)
            print "%s pass" %(stockid)
        except:
            print traceback.format_exc()
            continue

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'besttrader.html')

    for stockid in report.iter_symbol():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "besttrader_%s.html" % (stockid))

    # plot
    for stockid in report.iter_symbol():
        try:
            perf = report.pool[stockid]
            fig = plt.figure()
            ax1 = fig.add_subplot(211, ylabel='portfolio value')
            perf.portfolio_value.plot(ax=ax1)

            ax2 = fig.add_subplot(212)
            perf[['close']].plot(ax=ax2)

            ax2.plot(perf.ix[perf.buy].index, perf.close[perf.buy],
                     '^', markersize=10, color='m')
            ax2.plot(perf.ix[perf.sell].index, perf.close[perf.sell],
                     'v', markersize=10, color='k')
            plt.legend(loc=0)
            plt.gcf().set_size_inches(18, 8)
            plt.savefig("besttrader_%s_%s.png" %(traderid, stockid))
            #plt.show()
        except:
            continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test besttrader algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store', type=str, default='twse', help='twse/otc')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    #proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    #close_main_service(proc, args.debug)
