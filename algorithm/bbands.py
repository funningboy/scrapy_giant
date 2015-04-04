# -*- coding: utf-8 -*-

import pytz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pylab
import talib
import traceback

from datetime import datetime, timedelta
from collections import deque
from matplotlib.dates import date2num, DateFormatter
from matplotlib.finance import candlestick_ohlc
import matplotlib.ticker as mticker

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *
from talib import MA_Type

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler

from algorithm.report import Report


class BBandsAlgorithm(TradingAlgorithm):
    """
    sell after buy
    ref:
    http://pythonprogramming.net/advanced-matplotlib-graphing-charting-tutorial/
    """

    def __init__(self, dbhandler, *args, **kwargs):
        self.maxlen = kwargs.pop('maxlen', 70)
        self.maxhold = kwargs.pop('maxhold', 5)
        super(BBandsAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids
        self.tids = self.dbhandler.trader.ids

    def initialize(self):
        self.window = deque(maxlen=self.maxlen)
        self.invested = False
        self.hold = 0

    def handle_data(self, data):
        self.window.append((
            data[self.sids[0]].open,
            data[self.sids[0]].high,
            data[self.sids[0]].low,
            data[self.sids[0]].close,
            data[self.sids[0]].volume
        ))

        if len(self.window) == self.maxlen:
            open, high, low, close, volume = [np.array(i) for i in zip(*self.window)]
            upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)
            upper_bb, lower_bb = close - upper, close - lower
            upper_bb, lower_bb = upper_bb[~np.isnan(upper_bb)], lower_bb[~np.isnan(lower_bb)]
            h_idx, l_idx = np.argmax(upper_bb), np.argmin(lower_bb)
            rule_idx = h_idx + self.maxlen//3 <= l_idx and l_idx + 15 <= self.maxlen
            rule_inbb = close[-1] >= middle[-1] * 0.8 and close[-1] <= middle[-1] * 1.2
            rule_hidd = close[-1] == open[-1]

            if self.hold > 0:
                self.hold = self.hold - 1

            if rule_idx and rule_inbb and rule_hidd and self.invested == False:
                self.order(self.sids[0], 1000)
                self.invested = True
                self.hold = self.maxhold
            elif self.invested == True and self.hold == 0:
                self.order(self.sids[0], -1000)

            # save to recorder
            signals = {
                'open': open[-1],
                'high': high[-1],
                'low': low[-1],
                'close': close[-1],
                'volume': volume[-1],
                'upper': upper[-1],
                'middle': middle[-1],
                'lower': lower[-1]
            }
            self.record(**signals)


def run(opt='twse', debug=False, limit=0):
    # set time window
    maxlen = 30
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
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
            data = dbhandler.transform_all_data(starttime, endtime, [stockid], [], 'totalvolume', 10)
            if len(data[stockid].index) < maxlen:
                continue
            bbands = BBandsAlgorithm(dbhandler=dbhandler, maxlen=maxlen)
            results = bbands.run(data).fillna(0)
            report.collect(stockid, results)
            print "%s" %(stockid)
        except:
            print traceback.format_exc()
            continue

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'bbands.html')

    for stockid in report.iter_stockid():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "bbands_%s.html" % (stockid))

    for stockid in report.iter_stockid():
        perf = report.pool[stockid]
        dates = [date2num(i) for i in perf.index[maxlen:]]
        quotes = [perf[label][maxlen:].values for label in ['open', 'high', 'low', 'close']]
        quotes = zip(*([dates]+quotes))

        fig = plt.figure(facecolor='#07000d')

        ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
        candlestick_ohlc(ax1, quotes, width=.6, colorup='#53c156', colordown='#ff1717')

        ax1.plot(dates, perf['upper'][maxlen:].values,  '#e1edf9', label='upper',  linewidth=1.5)
        ax1.plot(dates, perf['middle'][maxlen:].values, '#e1edf9', label='middle', linewidth=1.5)
        ax1.plot(dates, perf['lower'][maxlen:].values,  '#e1edf9', label='lower',  linewidth=1.5)

        ax1.grid(True, color='w')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel('Stock price and Volume')

        bbLeg = plt.legend(loc=9, ncol=2, prop={'size':7}, fancybox=True, borderaxespad=0.)
        bbLeg.get_frame().set_alpha(0.4)
        textEd = pylab.gca().get_legend().get_texts()
        pylab.setp(textEd[0:6], color = 'w')

        ax1v = ax1.twinx()
        ax1v.fill_between(dates, 0, perf['volume'][maxlen:].values, facecolor='#00ffe8', alpha=.4)
        ax1v.axes.yaxis.set_ticklabels([])
        ax1v.grid(False)
        ###Edit this to 3, so it's a bit larger
        ax1v.set_ylim(0, 3*perf['volume'][maxlen:].values.max())
        ax1v.spines['bottom'].set_color("#5998ff")
        ax1v.spines['top'].set_color("#5998ff")
        ax1v.spines['left'].set_color("#5998ff")
        ax1v.spines['right'].set_color("#5998ff")
        ax1v.tick_params(axis='x', colors='w')
        ax1v.tick_params(axis='y', colors='w')

        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
        plt.gcf().set_size_inches(18, 8)
        plt.savefig("bbands_%s.png" %(stockid), facecolor=fig.get_facecolor())
#        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test bbands algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store', type=str, default='twse', help='twse/otc')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    close_main_service(proc, args.debug)
