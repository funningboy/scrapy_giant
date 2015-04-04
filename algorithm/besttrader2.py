# -*- coding: utf-8 -*-

import pytz
import matplotlib.pyplot as plt
import traceback

from matplotlib.collections import LineCollection
from sklearn import cluster, covariance, manifold

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from datetime import datetime, timedelta
from collections import deque

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from algorithm.report import Report


class BestTraderAlgorithm2(TradingAlgorithm):
    """
    find the best correlation between trader and stocks
    ref: http://scikit-learn.org/stable/auto_examples/applications/plot_stock_market.html
    https://www.quantopian.com/posts/working-with-history-dataframes
    """

    def __init__(self, dbhandler, *args, **kwargs):
        self.maxlen =  kwargs.pop('maxlen', 70)
        super(BestTraderAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids
        self.tids = self.dbhandler.trader.ids

    def initialize(self):
        self.edge_model = covariance.GraphLassoCV()
        self.window = deque(max_len=self.maxlen)
        self.X = deque(maxlen=self.maxlen*2)
        self.Y = deque(maxlen=self.maxlen*2)

    def handle_data(self, data):
#        data[self.sids[0]].top0_buyvolume
#        data[self.sids[0]].top0_sellvolume
#        data[self.sids[0]].top0_price
        self.window.append((data[self.sids[0]].price, data[self.sids[0]].top0_price))

        if len(self.window) == 30:
            # standardize the time series
            sid_p, tid_p = zip(*self.window)
            sid_p = np.array(sid_p).astype(np.float)
            tid_p = np.array(tid_p).astype(np.float)
            variation = sid_p - tid_p
            X = variation.copy().T
            X /= X.std(axis=0)
            self.edge_model.fit(X)

            # Cluster using affinity propagation
            _, labels = cluster.affinity_propagation(self.edge_model.covariance_)
            n_labels = labels.max()
            for i in range(n_labels + 1):
                print('Cluster %i: %s' % ((i + 1), ', '.join(names[labels == i])))

            # Find a low-dimension embedding for visualization: find the best position of
            # the nodes (the stocks) on a 2D plane
            node_position_model = manifold.LocallyLinearEmbedding(
                n_components=2, eigen_solver='dense', n_neighbors=6)
            embedding = node_position_model.fit_transform(X.T).T

            # save to recorder
            signals = {
            }

            self.record(**signals)


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    # set time window
    starttime = datetime.utcnow() - timedelta(days=30)
    endtime = datetime.utcnow()
    # sort factor
    report = Report(
        sort=[('buy_count', False), ('sell_count', False), ('volume', False)], limit=20)
    # set debug or normal mode
    kwargs = {
        'debug': debug,
        'limit': limit,
        'opt': opt
    }
    # 1590:u'花旗環球', 1440:u'美林'
    traderid = '1440'
    idhandler = TwseIdDBHandler() if kwargs['opt'] == 'twse' else OtcIdDBHandler()
    for stockid in idhandler.stock.get_ids(**kwargs):
        try:
            dbhandler = TwseHisDBHandler() if kwargs['opt'] == 'twse' else OtcHisDBHandler()
            dbhandler.stock.ids = [stockid]
            data = dbhandler.transform_all_data(starttime, endtime, [stockid], [traderid], 'totalvolume', 10)
            besttrader = BestTraderAlgorithm(dbhandler=dbhandler)
            results = besttrader.run(data).fillna(0)
            report.collect(stockid, results)
            print "%s pass" %(stockid)
        except:
            print traceback.format_exc()
            continue

    if report.report.empty:
        return

#    # report summary
#    stream = report.summary(dtype='html')
#    report.write(stream, 'besttrader_%s.html' % (traderid))
#
#    for stockid in report.iter_stockid():
#        stream = report.iter_report(stockid, dtype='html')
#        report.write(stream, "besttrader_%s.html" % (traderid, stockid))

    # plot
    for stockid in report.iter_stockid():
        try:
            perf = report.pool[stockid]
        except:
            continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test besttrader algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store_true', default='twse', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    close_main_service(proc, args.debug)
