# -*- coding: utf-8 -*-

#%matplotlib inline
#import pyfolio as pf

import pytz
import matplotlib.pyplot as plt
import numpy as np
import talib
import traceback

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *
from zipline.finance.trading import SimulationParameters

# Import exponential moving average from talib wrapper
# ref: http://mrjbq7.github.io/ta-lib/doc_index.html

from datetime import datetime, timedelta
from collections import deque

from bin.mongodb_driver import *
from bin.start import *
from handler.tasks import collect_hisframe
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler

from algorithm.report import Report
from algorithm.register import AlgRegister

class DualEMA(TradingAlgorithm):
    """ Dual Moving Average Crossover algorithm.
    buy:
    sell:
    """

    def __init__(self, dbhandler, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._cfg = {
            'buf_win': kwargs.pop('buf_win', 30),
            'buy_hold': kwargs.pop('buy_hold', 5),
            'sell_hold': kwargs.pop('sell_hold', 5),
            'buy_amount': kwargs.pop('buy_amount', 1000),
            'sell_amount': kwargs.pop('sell_amount', 1000),
            'short_ema_win': kwargs.pop('short_ema_win', 7),
            'long_ema_win': kwargs.pop('long_ema_win', 20),
            'trend_up': kwargs.pop('trend_up', True),
            'trend_down': kwargs.pop('trend_down', True)
        }
        super(DualEMA, self).__init__(**kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids

    @property
    def cfg(self):
        return self._cfg

    def initialize(self):
        self.window = deque(maxlen=self._cfg['buf_win'])
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
            short_ema = talib.EMA(close, timeperiod=self._cfg['short_ema_win'])
            long_ema = talib.EMA(close, timeperiod=self._cfg['long_ema_win'])
            real_obv = talib.OBV(close, np.asarray(volume, dtype='float'))

            self.buy_hold = self.buy_hold - 1 if self.buy_hold > 0 else self.buy_hold
            self.sell_hold = self.sell_hold - 1 if self.sell_hold > 0 else self.sell_hold
            self.buy = False
            self.sell = False

            # sell after buy
            if self._cfg['trend_up']:
                if short_ema[-1] > long_ema[-1] and not self.invested_buy:
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
                if short_ema[-1] < long_ema[-1] and not self.invested_sell:
                    self.order(sid, -self._cfg['sell_amount'])
                    self.invested_sell = True
                    self.sell = True
                    self.sell_hold = self._cfg['sell_hold']
                elif self.invested_sell == True  and self.sell_hold == 0:
                    self.order(sid, self._cfg['sell_amount'])
                    self.invested_sell = False
                    self.buy = True

            # save to recorder
            signals = {
                'open': open[-1],
                'high': high[-1],
                'low': low[-1],
                'close': close[-1],
                'volume': volume[-1],
                'short_ema': short_ema[-1],
                'long_ema': long_ema[-1],
                'buy': self.buy,
                'sell': self.sell
            }
            self.record(**signals)

# register to alg tasks
AlgRegister.add(DualEMA)

def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    maxlen = 30
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    report = Report(
        'dualema',
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
                'targets': ['stock'],
                'starttime': starttime,
                'endtime': endtime,
                'stockids': [stockid],
                'traderids': [],
                'base': 'stock',
                'callback': None,
                'limit': 1,
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

            dualema = DualEMA(dbhandler=dbhandler, debug=debug, sim_params=sim_params)
            results = dualema.run(panel).fillna(0)
            risks = dualema.perf_tracker.handle_simulation_end()  
            report.collect(stockid, results, risks)
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
