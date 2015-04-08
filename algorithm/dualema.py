# -*- coding: utf-8 -*-

import pytz
import matplotlib.pyplot as plt
import traceback

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

# Import exponential moving average from talib wrapper
# ref: http://mrjbq7.github.io/ta-lib/doc_index.html
from zipline.transforms.ta import EMA, OBV

from datetime import datetime, timedelta

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from algorithm.report import Report


class DualEMAAlgorithm(TradingAlgorithm):
    """ Dual Moving Average Crossover algorithm.

    This algorithm buys apple once its short moving average crosses
    its long moving average (indicating upwards momentum) and sells
    its shares once the averages cross again (indicating downwards
    momentum).

    """

    def __init__(self, dbhandler, *args, **kwargs):
        super(DualEMAAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids

    def initialize(self):
        self.short_ema_trans = EMA(timeperiod=20)
        self.long_ema_trans = EMA(timeperiod=40)
        self.real_obv_trans = OBV()
        self.invested = False

    def __repr__(self):
        return ""

    def handle_data(self, data):
        self.short_ema = self.short_ema_trans.handle_data(data)
        self.long_ema = self.long_ema_trans.handle_data(data)
        self.real_obv = self.real_obv_trans.handle_data(data)
        if self.short_ema is None or self.long_ema is None or self.real_obv is None:
            return

        self.buy = False
        self.sell = False

        # buy/sell rule
        if (self.short_ema > self.long_ema).all() and not self.invested:
            self.order(self.sids[0], 1000)
            self.invested = True
            self.buy = True
        elif (self.short_ema < self.long_ema).all() and self.invested:
            self.order(self.sids[0], -1000)
            self.invested = False
            self.sell = True

        # save to recorder
        signals = {
            'open': data[self.sids[0]].open,
            'high': data[self.sids[0]].high,
            'low': data[self.sids[0]].low,
            'close': data[self.sids[0]].close,
            'volume': data[self.sids[0]].volume,
            'short_ema': self.short_ema[self.sids[0]],
            'long_ema': self.long_ema[self.sids[0]],
            'buy': self.buy,
            'sell': self.sell
        }
        self.record(**signals)

def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    # set time window
    maxlen = 30
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
            dbhandler.trader.ids = []
            data = dbhandler.transform_all_data(starttime, endtime, [stockid], [], 'totalvolume', 10)
            if len(data[stockid].index) < maxlen:
                continue
            dualema = DualEMAAlgorithm(dbhandler=dbhandler)
            results = dualema.run(data).fillna(0)
            report.collect(stockid, results)
            print "%s pass" %(stockid)
        except:
            print traceback.format_exc()
            continue

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'dualema.html')

    print report.summary(dtype='dict')

    for stockid in report.iter_stockid():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "dualema_%s.html" % (stockid))

    # plot
    for stockid in report.iter_stockid():
        try:
            perf = report.pool[stockid]
            fig = plt.figure()
            ax1 = fig.add_subplot(211, ylabel='portfolio value')
            perf.portfolio_value.plot(ax=ax1)

            ax2 = fig.add_subplot(212)
            perf[['short_ema', 'long_ema']].plot(ax=ax2)

            ax2.plot(perf.ix[perf.buy].index, perf.short_ema[perf.buy],
                     '^', markersize=10, color='m')
            ax2.plot(perf.ix[perf.sell].index, perf.short_ema[perf.sell],
                     'v', markersize=10, color='k')
            plt.legend(loc=0)
            plt.gcf().set_size_inches(18, 8)
            plt.savefig("dualema_%s.png" %(stockid))
            #plt.show()
        except:
            continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test dualema algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store', type=str, default='twse', help='twse/otc')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    close_main_service(proc, args.debug)
