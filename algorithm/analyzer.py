# -*- coding: utf-8 -*-

import numpy as np
import talib
import traceback

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

# Import exponential moving average from talib wrapper
# ref: http://mrjbq7.github.io/ta-lib/doc_index.html

from datetime import datetime, timedelta
from collections import deque

from bin.mongodb_driver import *
from bin.start import *
from handler.tasks import collect_hisframe
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler

from algorithm.report import Report


class Analyzer():

    def __init__(self, dbhandler, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._buf_win = kwargs.pop('buf_win', 30)
        self._trend_up = kwargs.pop('trend_up', False)
        self._trend_down = kwargs.pop('trend_down', False)
        self._up_ratio = kwargs.pop('up_ratio', 30)
        self._down_ratio = kwargs.pop('down_ratio', 30)
        self._max_up = kwargs.pop('max_up', 3)
        self._max_down = kwargs.pop('max_down', 3)
        super(Analyzer, self).__init__(**kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids
        self.tids = self.dbhandler.trader.ids
        self.tops = list(self.dbhandler.trader.get_alias([self.sids[0]], 'trader', ["top%d" %i for i in range(10)]))
        if self._debug:
            print self.tops

    def initialize(self):
        self.window = deque(maxlen=self._buf_win)

    def handle_data(self, data):
        sid = self.sids[0]
        tmptop = []

        for i in range(10):
            tmptop.append((self.topsgetattr(data[sid], "top%d_buyvolume" %(i)) - getattr(data[sid], "top%d_sellvolume" %(i), self.tops[i])))

        self.window.append((
            # data
            data[sid].open,
            data[sid].high,
            data[sid].low,
            data[sid].close,
            data[sid].volume,
            # future
            data[sid].fopen,
            data[sid].fhigh,
            data[sid].flow,
            data[sid].fclose,
            data[sid].fvolume,
            # credit
            data[sid].financesellvolume,
            data[sid].financeused
        ))
        self.window[-1] += (tmptop[-1],)

        if len(self.window) == self._buf_win:
            open, high, low, close, volume = [np.array(i) for i in zip(*self.window)]
   
            talib.EMA(close, timeperiod=5)
            talib.OBV(close, np.asarray(volume, dtype='float'))
            #talib.DMA


        if self._trend_up:
            close[-1]

        signals = {
            'open': open[-1],

        }


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    maxlen = 5
    starttime = datetime.utcnow() - timedelta(days=15)
    endtime = datetime.utcnow()

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
            # pre find traderid as top0
            kwargs = {
                'opt': opt,
                'targets': ['trader'],
                'starttime': starttime,
                'endtime': endtime,
                'stockids': [stockid],
                'traderids': [],
                'base': 'stock',
                'order': [],
                'callback': None,
                'limit': 10,
                'debug': True
            }
            panel, dbhandler = collect_hisframe(**kwargs)
            tops = list(dbhandler.trader.get_alias([stockid], 'trader', ["top%d" %i for i in range(10)]))
            print "prefound:%s" %(tops)
            traderid = tops[0] if traderid not in tops else traderid
            # run
            kwargs = {
                'opt': opt,
                'targets': ['stock', 'trader', 'future', 'credit'],
                'starttime': starttime,
                'endtime': endtime,
                'stockids': [stockid],
                'traderids': [traderid],
                'base': 'trader',
                'order': [],
                'callback': None,
                'limit': 10,
                'debug': True
            }
            panel, dbhandler = collect_hisframe(**kwargs)
            if len(panel[stockid].index) < maxlen:
                continue
            besttrader = BestTraderAlgorithm(dbhandler=dbhandler, debug=debug)
            results = besttrader.run(panel).fillna(0)
            report.collect(stockid, results)
            print "%s pass" %(stockid)
        except:
            print traceback.format_exc()
            continue

    if report.report.empty:
        return