# -*- coding: utf-8 -*-

import pytz

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

# Import exponential moving average from talib wrapper
# ref: http://mrjbq7.github.io/ta-lib/doc_index.html
from zipline.transforms.ta import EMA, OBV

from datetime import datetime, timedelta

from bin.mongodb_driver import *
from bin.start import *
from query.hisdb_query import *
from query.iddb_query import *
from algorithm.report import Report


class DualEMATaLib(TradingAlgorithm):
    """ Dual Moving Average Crossover algorithm.

    This algorithm buys apple once its short moving average crosses
    its long moving average (indicating upwards momentum) and sells
    its shares once the averages cross again (indicating downwards
    momentum).

    """

    def __init__(self, dbquery, *args, **kwargs):
        super(DualEMATaLib, self).__init__(*args, **kwargs)
        self.dbquery = dbquery
        self.mstockid = self.dbquery._stockmap.keys()[0]

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

        try:
            # add sideband siganl
            signals.update({
                'topbuy0_%s' % (self.dbquery.stockmap(self.mstockid, 'topbuy0')): data[self.mstockid].topbuy0,
                'topsell0_%s' % (self.dbquery.stockmap(self.mstockid, 'topsell0')): data[self.mstockid].topsell0
            })
        except:
            pass
        self.record(**signals)

def main(debug=False, limit=0):
    proc = start_service(debug)
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
        'limit': limit
    }
    for stockid in TwseIdDBQuery().get_stockids(**kwargs):
        dbquery = TwseHisDBQuery()
        data = dbquery.get_all_data(
            starttime=starttime, endtime=endtime,
            stockids=[stockid], traderids=[])
        if data.empty:
            continue
        dualema = DualEMATaLib(dbquery=dbquery)
        results = dualema.run(data).fillna(0)
        if results.empty:
            continue
        report.collect(stockid, results)
        print stockid

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'dualema.html')

    for stockid in report.iter_stockid():
        report.iter_report(stockid, dtype='html')

    close_service(proc, debug)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test dualema algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', help='debug mode')
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    main(debug=True if args.debug else False, limit=args.limit)
