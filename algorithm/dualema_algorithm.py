# -*- coding: utf-8 -*-

import pytz
import matplotlib.pyplot as plt

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


class DualEMATaLib(TradingAlgorithm):
    """ Dual Moving Average Crossover algorithm.

    This algorithm buys apple once its short moving average crosses
    its long moving average (indicating upwards momentum) and sells
    its shares once the averages cross again (indicating downwards
    momentum).

    """

    def __init__(self, dbhandler, *args, **kwargs):
        super(DualEMATaLib, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.mstockid = self.dbhandler.stock.ids[0]

    def initialize(self, short_window=20, long_window=40):
        # Add 2 mavg transforms, one with a long window, one
        # with a short window.
        self.short_ema_trans = EMA(timeperiod=short_window)
        self.long_ema_trans = EMA(timeperiod=long_window)
        self.real_obv_trans = OBV()

        # To keep track of whether we invested in the stock or not
        self.invested = False

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
            self.order(self.mstockid, 1000)
            self.invested = True
            self.buy = True
        elif (self.short_ema < self.long_ema).all() and self.invested:
            self.order(self.mstockid, -1000)
            self.invested = False
            self.sell = True

        # save to recorder
        signals = {
            'open': data[self.mstockid].open,
            'high': data[self.mstockid].high,
            'low': data[self.mstockid].low,
            'close': data[self.mstockid].close,
            'volume': data[self.mstockid].volume,
            'short_ema': self.short_ema[self.mstockid],
            'long_ema': self.long_ema[self.mstockid],
            'buy': self.buy,
            'sell': self.sell
        }

        self.record(**signals)


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    # set time window
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    # sort factor
    report = Report(
        algname=DualEMATaLib.__name__,
        sort=[('buy_count', False), ('sell_count', False), ('volume', False)], limit=20)
    # set debug or normal mode
    kwargs = {
        'debug': debug,
        'limit': limit,
        'opt': opt
    }
    idhandler = TwseIdDBHandler() if kwargs['opt'] == 'twse' else OtcIdDBHandler()
    for stockid in idhandler.stock.get_ids(**kwargs):
        dbhandler = TwseHisDBHandler() if kwargs['opt'] == 'twse' else OtcHisDBHandler()
        dbhandler.stock.ids = [stockid]
        data = dbhandler.transform_all_data(starttime, endtime, [stockid], [], 10)
        if data.empty:
            continue
        dualema = DualEMATaLib(dbhandler=dbhandler)
        results = dualema.run(data).fillna(0)
        if results.empty:
            continue
        report.collect(stockid, results)
        print stockid

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'dualema.html')

    for stockid in report.iter_stockid():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "dualema_%s.html" % (stockid))

        # plt
        fig = plt.figure()
        ax1 = fig.add_subplot(211, ylabel='portfolio value')
        results.portfolio_value.plot(ax=ax1)

        ax2 = fig.add_subplot(212)
        results[['short_ema', 'long_ema']].plot(ax=ax2)

        ax2.plot(results.ix[results.buy].index, results.short_ema[results.buy],
                 '^', markersize=10, color='m')
        ax2.plot(results.ix[results.sell].index, results.short_ema[results.sell],
                 'v', markersize=10, color='k')
        plt.legend(loc=0)
        plt.gcf().set_size_inches(18, 8)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test dualema algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    proc = start_main_service(args.debug)
    run('twse', args.debug, args.limit)
    close_main_service(proc, args.debug)
