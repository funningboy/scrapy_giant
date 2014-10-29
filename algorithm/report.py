# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from datetime import datetime, timedelta
from collections import OrderedDict

class Report(object):

    def __init__(self, algname, sort=[('ending_value', 1)], limit=10):
        self._algnm = algname
        self._limit = limit
        self._sort, self._direct = zip(*sort)
        self._report = pd.DataFrame()
        self._pool = OrderedDict()

    def collect(self, stockid, results):
        item = {
            'date': results.index[-1],
            'open': results['open'].values[-1],
            'high': results['high'].values[-1],
            'low': results['low'].values[-1],
            'close': results['close'].values[-1],
            'volume': results['volume'].values[-1],
            'ending_value': results['ending_value'].mean()
        }
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

    def iter_report(self, stockid, dtype='json'):
        if dtype == 'json':
            return self._pool[stockid].to_json()
        elif dtype == 'html':
            return self._pool[stockid].to_html()
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
        if dtype == 'json':
            return self._report.to_json()
        elif dtype == 'html':
            return self._report.to_html()
        else:
            return self._report

    def write(self, stream, filenm):
        f = open(filenm, 'w')
        f.write(stream)
        f.close()

