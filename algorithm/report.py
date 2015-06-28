# -*- coding: utf-8 -*-
# http://www.amcharts.com/tips/using-html-table-data-provider-chart/
import numpy as np
import pandas as pd
import re

from datetime import datetime, timedelta
from collections import OrderedDict

class Report(object):

    def __init__(self, sort=[('ending_value', 1)], limit=10):
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

    def collect(self, symbol, results):
        # ref:
        # https://github.com/quantopian/zipline/blob/7892a6943f7b027be1e3c5a75eac61e7c4c0a027/zipline/finance/performance/period.py
        # collect and sort results as df
        item = OrderedDict({
            'bufwin': (results.index[-1] - results.index[0]).days,
            'date': results.index[-1] if len(results.index) > 0 else datetime.utcnow(),
            'buys': results['buy'].sum() if 'buy' in results.columns else 0,
            'sells': results['sell'].sum() if 'sell' in results.columns else 0,
            # zipline key
            'portfolio_value': results['portfolio_value'][-1] if 'portfolio_value' in results.columns else 0,
            'ending_value': results['ending_value'][-1] if 'ending_value' in results.columns else 0,
            'ending_cash': results['ending_cash'][-1] if 'ending_cash' in results.columns else 0,
            'capital_used': results['capital_used'][-1] if 'capital_used' in results.columns else 0
        })
        frame = pd.DataFrame.from_dict({symbol: item}).fillna(0)
        self._report = pd.concat([self._report, frame.T], axis=0).fillna(0).sort(columns=list(self._sort), ascending=list(self._direct))[0:self._limit]
        self._pool.update({symbol: results})
        rms = [it for it in self._pool if it not in self._report.index]
        for it in rms:
            del self._pool[it]

    def iter_symbol(self):
        for symbol in self._report.index:
            yield symbol

    def iter_report(self, symbol, dtype=None):
        if symbol not in self._pool:
            return pd.DataFrame()
        columns = self._pool[symbol].columns
        if dtype == 'json':
            return self._pool[symbol].to_json()
        elif dtype == 'html':
            return self._pool[symbol].to_html(columns=columns)
        elif dtype == 'dict':
            return self._pool[symbol].to_dict()
        else:
            return self._pool[symbol]

    def summary(self, dtype=None):
        """
        dtype == 'json|html|pd.frame|dict' ...
        <algorithm name>
        <datetime>
               portfolio_value | buy | sell|
        2330    11             | 10  |   0 |
        2317    10             |  1  |   1 |
        """
        columns = self._report.columns
        if dtype == 'json':
            return self._report.to_json()
        elif dtype == 'html':
            return self._report.to_html(columns=columns)
        elif dtype == 'dict':
            return self._report.to_dict()
        else:
            return self._report

    def write(self, stream, filenm):
        f = open(filenm, 'w')
        f.write(stream)
        f.close()

