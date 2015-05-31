# -*- coding: utf-8 -*-
# ref: http://scikit-learn.org/stable/auto_examples/applications/plot_stock_market.html
# https://www.quantopian.com/posts/working-with-history-dataframes

import pandas as pd
import pytz
import matplotlib.pyplot as plt
import traceback

from matplotlib.collections import LineCollection
from sklearn import cluster, covariance, manifold

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *
from zipline.finance.execution import LimitOrder

from datetime import datetime, timedelta
from collections import deque

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from algorithm.report import Report


class BestTraderAlgorithm(TradingAlgorithm):
    """ find the best correlation between trader and stocks
    buy:
    sell:
    """

    def __init__(self, dbhandler, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._buf_win = kwargs.pop('buf_win', 10)
        super(BestTraderAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids
        self.tids = self.dbhandler.trader.ids
        self.tops = list(self.dbhandler.trader.get_alias([self.sids[0]], 'trader', ["top%d" %i for i in range(10)]))
        self.tops = {k:v for v,k in enumerate(self.tops)}
        if self._debug:
            print self.tops

    def initialize(self):
        self.window = deque(maxlen=self._buf_win)

    def handle_data(self, data):
        buyvolume, sellvolume = 0,0
        sideband = {}
        date = data[self.sids[0]].datetime

        try:
            buyvolume = getattr(data[self.sids[0]], "top%d_buyvolume" %(self.tops[self.tids[0]]))
            sellvolume = getattr(data[self.sids[0]], "top%d_sellvolume" %(self.tops[self.tids[0]]))
            avgbuyprice = getattr(data[self.sids[0]], "top%d_avgbuyprice" %(self.tops[self.tids[0]]))
            avgsellprice = getattr(data[self.sids[0]], "top%d_avgsellprice" %(self.tops[self.tids[0]]))
            ratio = getattr(data[self.sids[0]], "top%d_ratio" %(self.tops[self.tids[0]]))

            if buyvolume:
                self.order_target_percent(self.sids[0], buyvolume, style=LimitOrder(avgbuyprice))
            if sellvolume:
                self.order_target_percent(self.sids[0], -sellvolume, style=LimitOrder(avgsellprice))

            sideband = {
                "top%d_%s_buyvolume" % (self.tops[self.tids[0]], self.tids[0]): buyvolume,
                "top%d_%s_sellvolume" % (self.tops[self.tids[0]], self.tids[0]): sellvolume,
                "top%d_%s_avgbuyprice" % (self.tops[self.tids[0]], self.tids[0]): avgbuyprice,
                "top%d_%s_avgsellprice" % (self.tops[self.tids[0]], self.tids[0]): avgsellprice
            }
        except:
            if self._debug:
                print "%s: traderid(%s) not found in stockid(%s)" %(date, self.tids[0], self.sids[0])
        pass

        # save to recorder
        signals = {
            'open': data[self.sids[0]].open,
            'high': data[self.sids[0]].high,
            'low': data[self.sids[0]].low,
            'close': data[self.sids[0]].close,
            'volume': data[self.sids[0]].volume,
            'buy': True if buyvolume else False,
            'sell': True if sellvolume else False
        }

        # map sideband as signal
        signals.update(sideband)
        self.record(**signals)


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    # set time window
    maxlen = 5
    starttime = datetime.utcnow() - timedelta(days=15)
    endtime = datetime.utcnow()
    # sort factor
    report = Report(
        sort=[('buy_count', False), ('sell_count', False), ('portfolio_value', False)], limit=20)
    # set debug or normal mode
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
            kwargs = {
                'debug': True,
                'opt': opt
            }
            # pre find traderid as top0
            dbhandler = TwseHisDBHandler(**kwargs) if kwargs['opt'] == 'twse' else OtcHisDBHandler(**kwargs)
            args = (starttime, endtime, [stockid], [], 'stock', ['-totalvolume'], 10)
            dbhandler.trader.query_raw(*args)
            tops = list(dbhandler.trader.get_alias([stockid], 'trader', ["top%d" %i for i in range(10)]))
            print "prefound:%s" %(tops)
            traderid = tops[0] if traderid not in tops else traderid

            # main
            dbhandler = TwseHisDBHandler() if kwargs['opt'] == 'twse' else OtcHisDBHandler()
            dbhandler.stock.ids = [stockid]
            dbhandler.trader.ids = [stockid]
            # group sub df to main df
            args = (starttime, endtime, [stockid], [traderid], 'stock', ['-totalvolume'], 10, dbhandler.trader.to_pandas)
            traderdt = dbhandler.trader.query_raw(*args)
            args = (starttime, endtime, [stockid] , ['-totalvolume'], 10, dbhandler.stock.to_pandas)
            stockdt = dbhandler.stock.query_raw(*args)
            data = pd.concat([stockdt, traderdt], axis=2).fillna(0)
            if len(data[stockid].index) < maxlen:
                continue
            besttrader = BestTraderAlgorithm(dbhandler=dbhandler, debug=True)
            results = besttrader.run(data).fillna(0)
            report.collect(stockid, results)
            print "%s pass" %(stockid)
        except:
            print traceback.format_exc()
            continue

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'besttrader_%s.html' % (traderid))

    for stockid in report.iter_symbol():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "besttrader_%s_%s.html" % (traderid, stockid))

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
    parser.add_argument('--opt', dest='opt', action='store', type=str, help='twse/otc')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    #proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    #close_main_service(proc, args.debug)
