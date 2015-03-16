# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import numpy as np
import pylab as pl
import pytz
import matplotlib.pyplot as plt

from sklearn.hmm import GaussianHMM

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from bin.mongodb_driver import *
from bin.start import *
from query.hisdb_query import *
from query.iddb_query import *
from algorithm.report import Report


class GaussianHmmLib(TradingAlgorithm):
    """
    ref: http://scikit-learn.org/0.14/auto_examples/applications/plot_hmm_stock_analysis.html
    bear market: smaller mean, higher variant
    bull market: higher mean, smaller variant
    """

    def __init__(self, dbhandler, *args, **kwargs):
        super(GaussianHmmLib, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.mstockid = self.dbhandler.stock.ids[0]
        self.train = {
            'dates': np.array([]),
            'close_v': np.array([], dtype=float),
            'volume': np.array([], dtype=int)
        }
        self.test = {}
        self.hidden_states = None

    def initialize(self):
        self.invested = False

    def handle_data(self, data):
        self.train['dates'].append(data[self.mstockid].dt)
        self.train['close_v'].append(data[self.mstockid].price)
        self.train['volume'].append(data[self.mstockid].volume)

    def train_data(self):
        pass

    def test_data(self):
        pass

    def post_run(self, n_components=5):
        self.train['volume'] = self.train['volume'][1:]
        diff = self.train['close_v'][1:] - self.train['close_v'][:-1]
        X = np.column_stack([diff, self.train['volume']])
        model = GaussianHMM(n_components, covariance_type="diag", n_iter=1000)
        model.fit([X])
        self.hidden_states = model.predict(X)


def main(opt='twse', debug=False, limit=0):
    proc = start_service(debug)
    # set time window
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    # sort factor
    report = Report(
        algname=GaussianHmmLib.__name__,
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
        data = dbhandler.transform_all_data(starttime, endtime, [stockid], [], 'totalvolume', 10)
        if data.empty:
            continue
        hmm = GaussianHmmLib(dbhandler=dbhandler)
        hmm.run(data)
        hmm.post_run()
        #hmm.

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='train GaussianHmm algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', help='debug mode')
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    main(debug=True if args.debug else False, limit=args.limit)
