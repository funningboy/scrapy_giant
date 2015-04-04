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

    def collect(self, stockid, results):
        # collect and sort
        item = OrderedDict({
            'buy_count': results['buy'].sum() if 'buy' in results.columns else 0,
            'sell_count': results['sell'].sum() if 'sell' in results.columns else 0,
            'portfolio_value': results['portfolio_value'].mean() if 'portfilio_value' in results.columns else 0,
            'ending_value': results['ending_value'].sum() if 'ending_value' in results.columns else 0,
            'ending_cash': results['ending_cash'].mean() if 'ending_cash' in results.columns else 0,
            'volume': results['volume'].mean() if 'volume' in results.columns else 0
        })
        frame = pd.DataFrame.from_dict({stockid: item}).fillna(0)
        self._report = pd.concat([self._report, frame.T], axis=0).fillna(0).sort(columns=list(self._sort), ascending=list(self._direct))[0:self._limit]
        self._pool.update({stockid: results})
        rms = [it for it in self._pool if it not in self._report.index]
        for it in rms:
            del self._pool[it]

    def iter_stockid(self):
        for stockid in self._report.index:
            yield stockid

    def iter_report(self, stockid, dtype='json'):
        columns = self._pool[stockid].columns
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
        columns = self._report.columns
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

