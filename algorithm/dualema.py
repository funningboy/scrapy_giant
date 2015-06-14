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
    buy:
    sell:
    """

    def __init__(self, dbhandler, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._buf_win = kwargs.pop('buf_win', 30)
        self._short_ema_win = kwargs.pop('short_ema_win', 20)
        self._long_ema_win = kwargs.pop('long_ema_win', 40)
        self._buy_amount = kwargs.pop('buy_amount', 1000)
        self._sell_amount = kwargs.pop('sell_amount', 1000)
        super(DualEMAAlgorithm, self).__init__(**kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids

    def initialize(self):
        self.short_ema_trans = EMA(timeperiod=self._short_ema_win)
        self.long_ema_trans = EMA(timeperiod=self._long_ema_win)
        self.real_obv_trans = OBV()
        self.invested = False
        self.buy = False
        self.sell = False

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
            self.order(self.sids[0], self._buy_amount)
            self.invested = True
            self.buy = True
        elif (self.short_ema < self.long_ema).all() and self.invested:
            self.order(self.sids[0], -self._sell_amount)
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
    maxlen = 30
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    report = Report(
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
                'debug': debug,
                'opt': opt
            }
            dbhandler = TwseHisDBHandler(**kwargs) if kwargs['opt'] == 'twse' else OtcHisDBHandler(**kwargs)
            dbhandler.stock.ids = [stockid]
            args = (starttime, endtime, [stockid], 'stock', ['-totalvolume'], 10)
            cursor = dbhandler.stock.query_raw(*args)
            data = dbhandler.stock.to_pandas(cursor)
            if len(data[stockid].index) < maxlen:
                continue
            dualema = DualEMAAlgorithm(dbhandler=dbhandler, debug=debug)
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

    for stockid in report.iter_symbol():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "dualema_%s.html" % (stockid))

    # plot
    for stockid in report.iter_symbol():
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
    #proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    #close_main_service(proc, args.debug)
