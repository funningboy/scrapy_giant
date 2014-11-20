# -*- coding: utf-8 -*-

import pytz
import numpy as np
import pandas as pd

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *
from zipline.transforms.ta import EMA
from zipline.transforms.stddev import MovingStandardDev
from zipline.transforms.mavg import MovingAverage

from datetime import datetime, timedelta

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from algorithm.report import Report


class SuperManAlgorithm(TradingAlgorithm):
    """
    find the best buy point when the cur.volume >= volume.avg(10) and price.idxmax <= price.idxmin ...
    """

    def __init__(self, dbhandler, *args, **kwargs):
        super(SuperManAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        # main stockid, no reference stockids
        self.mstockid = self.dbhandler.stock.ids[0]

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
            alias_topbuy0 = self.dbhandler.trader.map_alias([self.mstockid], 'stock', ['topbuy0'])[0]
            alias_topsell0 = self.dbhandler.trader.map_alias([self.mstockid], 'stock', ['topsell0'])[0]
            signals.update({
                'topbuy0_%s' % (alias_topbuy0): data[self.mstockid].topbuy0,
                'topsell0_%s' % (alias_topsell0): data[self.mstockid].topsell0
            })
        except:
            pass
        self.record(**signals)


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
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
        supman = SuperManAlgorithm(dbhandler=dbhandler)
        results = supman.run(data).fillna(0)
        if results.empty:
            continue
        report.collect(stockid, results)
        print stockid

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'superman.html')

    for stockid in report.iter_stockid():
        stream = report.iter_report(stockid, dtype='html', has_other=True, has_sideband=True)
        report.write(stream, "superman_%s.html" % (stockid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test superman algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    proc = start_main_service(args.debug)
    run('twse', args.debug, args.limit)
    close_main_service(proc, args.debug)
