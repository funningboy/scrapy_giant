# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re

from datetime import datetime, timedelta
from collections import OrderedDict

class Report(object):

    def __init__(self, algname, sort=[('ending_value', 1)], limit=10):
        self._algnm = algname
        self._limit = limit
        self._sort, self._direct = zip(*sort)
        self._report = pd.DataFrame()
        self._pool = OrderedDict()

    @property
    def report(self):
        return self._report

    @property
    def pool(self):
        return self._pool

    def collect(self, stockid, results):
        # the latest date info
        item = OrderedDict({
            'date': results.index[-1],
            'buy': results['buy'].values[-1],
            'sell': results['sell'].values[-1],
            'buy_count': results['buy'].sum(),
            'sell_count': results['sell'].sum(),
            'portfolio_value': results['portfolio_value'].mean(),
            'ending_value': results['ending_value'].sum(),
            'ending_cash': results['ending_cash'].mean(),
            'open': results['open'].values[-1],
            'high': results['high'].values[-1],
            'low': results['low'].values[-1],
            'close': results['close'].values[-1],
            'volume': results['volume'].values[-1],
        })
        # summary
        frame = pd.DataFrame.from_dict({stockid: item}).fillna(0)
        self._report = pd.concat([self._report, frame.T], axis=0).fillna(0).sort(columns=list(self._sort), ascending=list(self._direct))[0:self._limit]
        # pool
        self._pool.update({stockid: results})
        rms = [it for it in self._pool if it not in self._report.index]
        for it in rms:
            del self._pool[it]

    def iter_stockid(self):
        for stockid in self._report.index:
            yield stockid

    def iter_report(self, stockid, dtype='json', has_other=False, has_sideband=False):
        others = []
        sidebands = []
        columns=[
            'buy',
            'sell',
            'portfolio_value',
            'ending_value',
            'ending_cash',
            'open',
            'high',
            'low',
            'close',
            'volume'
        ]
        for it in list(self._pool[stockid].columns.values):
            if re.match(r'top(buy|sell)\d+_\w+', it):
                sidebands.append(it)
            elif it not in columns:
                others.append(it)
        sidebands.sort()
        if has_other:
            columns.extend(others)
        if has_sideband:
            columns.extend(sidebands)

        if dtype == 'json':
            return self._pool[stockid].to_json(columns=columns)
        elif dtype == 'html':
            return self._pool[stockid].to_html(columns=columns)
        elif dtype == 'dict':
            return self._pool[stockid].to_dict(columns=columns)
        else:
            return self._pool[stockid]

    def summary(self, dtype='json'):
        """
        dtype == 'json|html|pd.frame|dict' ...
        <algorithm name>
        <datetime>
               portfolio_value | ... | open| high| low|close|volume|
        2330    11             | ... | 100 | 101 | 99 | 100 | 100  |
        2317    10             | ... | 100 | 102 | 98 | 99  | 99   |
        """
        columns=[
            'date',
            'buy',
            'sell',
            'buy_count',
            'sell_count',
            'portfolio_value',
            'ending_value',
            'ending_cash',
            'open',
            'high',
            'low',
            'close',
            'volume'
        ]

        if dtype == 'json':
            return self._report.to_json(columns=columns)
        elif dtype == 'html':
            return self._report.to_html(columns=columns)
        elif dtype == 'dict':
            return self._report.to_dict(columns=columns)
        else:
            return self._report

    def write(self, stream, filenm):
        f = open(filenm, 'w')
        f.write(stream)
        f.close()

