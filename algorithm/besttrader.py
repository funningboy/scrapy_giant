# -*- coding: utf-8 -*-
# ref: http://scikit-learn.org/stable/auto_examples/applications/plot_stock_market.html
# https://www.quantopian.com/posts/working-with-history-dataframes

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

    def __init__(self, dbhandler, *args, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._buf_win = kwargs.pop('buf_win', 10)
        super(BestTraderAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids
        self.tids = self.dbhandler.trader.ids
        self.tops = self.dbhandler.trader.map_alias([self.sids[0]], 'stock', ["top%d" %i for i in range(10)])
        self.tops = {k:v for v,k in enumerate(self.tops)}
        if self._debug:
            print self.tops

    def initialize(self):
        self.window = deque(maxlen=self._buf_win)

    def handle_data(self, data):
        buyvolume, sellvolume = 0,0
        sideband = {}
        try:
            buyvolume = getattr(data[self.sids[0]], "top%d_buyvolume" %(self.tops[self.tids[0]]))
            sellvolume = getattr(data[self.sids[0]], "top%d_sellvolume" %(self.tops[self.tids[0]]))
            price = getattr(data[self.sids[0]], "top%d_price" %(self.tops[self.tids[0]]))

            if buyvolume:
                self.order_target_percent(self.sids[0], buyvolume, style=LimitOrder(price))
            if sellvolume:
                self.order_target_percent(self.sids[0], -sellvolume, style=LimitOrder(price))

            sideband = {
                "top0_%s_buyvolume" % (self.tids[0]): buyvolume,
                "top0_%s_sellvolume" % (self.tids[0]): sellvolume,
                "top0_%s_price" % (self.tids[0]): price
            }
        except:
            if self._debug:
                print "traderid(%s) not found in stockid(%s)" %(self.tids[0], self.sids[0])
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
    starttime = datetime.utcnow() - timedelta(days=10)
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
    idhandler = TwseIdDBHandler() if kwargs['opt'] == 'twse' else OtcIdDBHandler()
    for stockid in idhandler.stock.get_ids(**kwargs):
        try:
            dbhandler = TwseHisDBHandler() if kwargs['opt'] == 'twse' else OtcHisDBHandler()
            dbhandler.stock.ids = [stockid]
            dbhandler.trader.ids = [traderid]
            data = dbhandler.transform_all_data(starttime, endtime, [stockid], [traderid], 'totalvolume', 10)
            if len(data[stockid].index) < maxlen:
                continue
            besttrader = BestTraderAlgorithm(dbhandler=dbhandler)
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

            ax2.plot(perf.ix[perf.buy].index,
                     '^', markersize=10, color='m')
            ax2.plot(perf.ix[perf.sell].index,
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
    proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    close_main_service(proc, args.debug)
