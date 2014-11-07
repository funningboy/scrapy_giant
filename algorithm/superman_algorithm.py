# -*- coding: utf-8 -*-

import pytz
import numpy as np

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *
from zipline.transforms.ta import EMA
from zipline.transforms.stddev import MovingStandardDev
from zipline.transforms.mavg import MovingAverage

from datetime import datetime, timedelta

from bin.mongodb_driver import *
from bin.start import *
from query.hisdb_query import *
from query.iddb_query import *
from algorithm.report import Report


class SuperManAlgorithm(TradingAlgorithm):
    """
    find the best buy point when the cur.volume >= volume.avg(10) and price.idxmax <= price.idxmin ...
    """

    def __init__(self, dbquery, *args, **kwargs):
        super(SuperManAlgorithm, self).__init__(*args, **kwargs)
        self.dbquery = dbquery
        # main stockid, no reference stockids
        self.mstockid = self.dbquery.stockmap.keys()[0]

    def initialize(self, short_window=5):
        # To keep track of whether we invested in the stock or not
        self.invested = False
        self.sample = []
        self.pool = []
        self.add_transform(MovingAverage, 'mavg', ['price', 'volume'], window_length=short_window)
        self.add_transform(MovingStandardDev, 'stddev', window_length=short_window)
        self.idxmin = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.idxmax = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.idxbuy = (pytz.timezone('UTC').localize(datetime.utcnow()), -1)
        self.idxsell = (pytz.timezone('UTC').localize(datetime.utcnow()), -1)
        self.stddev = (-1, -1)

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

        # sample for 5days period
        if len(self.pool) == 5:
            self.sample.append(self.pool[-1])
            self.pool = []
        self.pool.append((
            data[self.mstockid].dt,
            data[self.mstockid].price,
            data[self.mstockid].mavg.price,
            data[self.mstockid].stddev,
            data[self.mstockid].mavg.volume
        ))

        # caculate sample as 3*5 = 15days
        if len(self.sample) == 3:
            std_of_std = np.array([it[3] for it in self.sample if it[3]])
            std_of_avg = np.array([it[2] for it in self.sample if it[2]])
            self.stddev = (np.std(std_of_std), np.std(std_of_avg))
            self.sample.pop()

        self.buy = False
        self.sell = False

        # sell after buy
        # buyrule
        self.buy = \
            self.stddev[1] >= 0 and \
            self.stddev[1] < 0.3 and \
            data[self.mstockid].close >= data[self.mstockid].open * 1.04 and \
            data[self.mstockid].volume >= data[self.mstockid].mavg.volume * 2.5 and \
            self.idxmax[0] <= self.idxmin[0] - timedelta(30)

        #sellrule
        if self.invested:
            self.sell = data[self.mstockid].dt >= self.idxbuy[0] + timedelta(3)

        if self.buy and not self.invested:
            self.order(self.mstockid, 1000)
            self.invested = True
            self.buy = True
            self.sell = False
            self.idxbuy = (data[self.mstockid].dt, data[self.mstockid].price)
        elif self.sell and self.invested:
            self.order(self.mstockid, -1000)
            self.invested = False
            self.buy = False
            self.sell = True
            self.idxsell = (data[self.mstockid].dt, data[self.mstockid].price)

        # save to recorder
        signals = {
            'open': data[self.mstockid].open,
            'high': data[self.mstockid].high,
            'low': data[self.mstockid].low,
            'close': data[self.mstockid].close,
            'volume': data[self.mstockid].volume,
            'stddev': data[self.mstockid].stddev,
            'mavg': data[self.mstockid].mavg.price,
            'std_of_std' : self.stddev[0],
            'std_of_avg' : self.stddev[1],
            'buy': self.buy,
            'sell': self.sell
        }

        # add sideband signal
        try:
            signals.update({
                'topbuy0_%s' % (self.dbquery.find_stockmap(self.mstockid, 'topbuy0')): data[self.mstockid].topbuy0,
                'topsell0_%s' % (self.dbquery.find_stockmap(self.mstockid, 'topsell0')): data[self.mstockid].topsell0
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
        algname=SuperManAlgorithm.__name__,
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
        supman = SuperManAlgorithm(dbquery=dbquery)
        results = supman.run(data).fillna(0)
        if results.empty:
            continue
        report.collect(stockid, results)
        print stockid

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'superman.html')

    for stockid in report.iter_stockid():
        stream = report.iter_report(stockid, dtype='html', has_other=True)
        report.write(stream, "superman_%s.html" % (stockid))

    close_service(proc, debug)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test superman algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', help='debug mode')
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    main(debug=True if args.debug else False, limit=args.limit)
