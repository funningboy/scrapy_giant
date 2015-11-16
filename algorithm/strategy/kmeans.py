# -*- coding: utf-8 -*-
# ref: http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html

import pytz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
from collections import deque, Counter

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *
from zipline.finance.trading import SimulationParameters

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

from bin.mongodb_driver import *
from bin.start import *
from handler.tasks import collect_hisframe
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler

from algorithm.report import Report
from algorithm.register import AlgRegister

class Kmeans(TradingAlgorithm):

    def __init__(self, dbhandler, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._cfg = {
            'buf_win': kwargs.pop('buf_win', 15),
            'buy_hold': kwargs.pop('buy_hold', 5),
            'sell_hold': kwargs.pop('sell_hold', 5),
            'buy_amount': kwargs.pop('buy_amount', 1000),
            'sell_amount': kwargs.pop('sell_amount', 1000),        
            'samples': kwargs.pop('samples', 500),
            'trains': kwargs.pop('trains', 10),
            'tests': kwargs.pop('tests', 10),
            'trend_up': kwargs.pop('trend_up', True),
            'trend_down': kwargs.pop('trend_down', True),
            'score': kwargs.pop('score', 0.99)
        }
        super(Kmeans, self).__init__(**kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids

    @property
    def cfg(self):
        return self._cfg

    def initialize(self):
        self.window = deque(maxlen=self._cfg['buf_win'])
        self.X = deque(maxlen=self._cfg['samples'])
        self.Y = deque(maxlen=self._cfg['samples'])
        self.trained = False
        self.tested = False
        self.match = False
        self.invested_buy = False
        self.invested_sell = False
        self.buy = False
        self.sell = False
        self.buy_hold = 0
        self.sell_hold = 0

    def _bench_k_means(self, estimator, name, data, labels):
        t0 = time.time()
        estimator.fit(data)
        print('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
              % (name, (time.time() - t0), estimator.inertia_,
                 metrics.homogeneity_score(labels, estimator.labels_),
                 metrics.completeness_score(labels, estimator.labels_),
                 metrics.v_measure_score(labels, estimator.labels_),
                 metrics.adjusted_rand_score(labels, estimator.labels_),
                 metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
                 metrics.silhouette_score(data, estimator.labels_,
                                          metric='euclidean',
                                          sample_size=self._cfg['samples'])))

    def _classifier(self, data, labels):
        # cluster: 
        self._bench_k_means(KMeans(init='k-means++', n_clusters=2, n_init=10),
                          name="k-means++", data=data, labels=labels)

        self._bench_k_means(KMeans(init='random', n_clusters=2, n_init=10),
                          name="random", data=data, labels=labels)

        # in this case the seeding of the centers is deterministic, hence we run the
        # kmeans algorithm only once with n_init=1
        pca = PCA(n_components=2).fit(data)
        self._bench_k_means(KMeans(init=pca.components_, n_clusters=2, n_init=1),
                      name="PCA-based", data=data, labels=labels)
        print(79 * '_')

        ###############################################################################
        # Visualize the results on PCA-reduced data

        reduced_data = PCA(n_components=2).fit_transform(data)
        kmeans = KMeans(init='k-means++', n_clusters=2, n_init=10)
        kmeans.fit(reduced_data)

        # Step size of the mesh. Decrease to increase the quality of the VQ.
        h = .002     # point in the mesh [x_min, m_max]x[y_min, y_max].

        # Plot the decision boundary. For that, we will assign a color to each
        x_min, x_max = reduced_data[:, 0].min(), reduced_data[:, 0].max()
        y_min, y_max = reduced_data[:, 1].min(), reduced_data[:, 1].max()
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Obtain labels for each point in mesh. Use last dataed model.
        Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
        c = Counter(Z)

        if self._debug:
            # Put the result into a color plot
            Z = Z.reshape(xx.shape)

            plt.figure(1)
            plt.clf()
            plt.imshow(Z, interpolation='nearest',
                    extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                    cmap=plt.cm.Paired,
                    aspect='auto', origin='lower')

            plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
            # Plot the centroids as a white X
            centroids = kmeans.cluster_centers_
            plt.scatter(centroids[:, 0], centroids[:, 1],
                    marker='x', s=169, linewidths=3,
                    color='w', zorder=10)
            plt.title('K-means clustering on the stock  dataset (PCA-reduced data)\n'
                    'Centroids are marked with white cross')
            plt.xlim(x_min, x_max)
            plt.ylim(y_min, y_max)
            plt.xticks(())
            plt.yticks(())
            plt.savefig("kmeans_%s.png" %(self.sids[0]))
            #plt.show()

        if c[1] > c[0] * 1.5:
            print "market is too hot"
            return 0
        elif c[1] <= c[0] * 1.5 and c[1] > c[0] * 1.1:
            print "maket trend is up"
            return 1
        elif c[1] <= c[0] * 1.1 and c[1] >= c[0] * 0.9:
            print "market is in balance"
        elif c[1] <= c[0] * 0.9 and c[1] >= c[0] * 0.5:
            print "market trend is down"
            return 0
        elif c[1] < c[0] * 0.5:
            print "market is too cold"
            return 1

    def handle_data(self, data):
        self.window.append((
            data[self.sids[0]].open,
            data[self.sids[0]].high,
            data[self.sids[0]].low,
            data[self.sids[0]].close,
            data[self.sids[0]].volume
        ))

        if len(self.window) == self._cfg['buf_win']:
            open, high, low, close, volume = [np.array(i) for i in zip(*self.window)]
            changes = np.diff(close) / close[1:]

            # as train & target seqs
            # ex up(1): [0, 0 , 0, ...1, 1], down(0): [1, 1, 1, .. 0, 0]
            self.X.append(changes[:-1])
            self.Y.append(changes[-1] > 0)

            # train
            if not self.trained and not self.tested:
                if len(self.Y) == self._cfg['trains'] and len(self.X) == self._cfg['trains']:
                    X, y = np.array(list(self.X)), np.array(list(self.Y))
                    retval = self._classifier(X, y)

                    if retval == 1:
                        if self.invested_buy:
                            self.order(self.sids[0], sell._cfg['buy_amount'])
                            self.invested_buy = True
                            self.buy = True
                            self.buy_hold = self._cfg['buy_hold'] 
                        elif self.invested_buy == True and self.buy_hold == 0:
                            self.order(self.sids[0], -self._cfg['buy_amount'])
                            self.invested_buy = False
                            self.sell = True

                    # buy after sell
                    if retval == 0:
                        if self.invested_sell:
                            self.order(self.sids[0], -self._cfg['sell_amount'])
                            self.invested_sell = True
                            self.sell = True
                            self.sell_hold = self._cfg['sell_hold']
                        elif self.invested_sell == True  and self.sell_hold == 0:
                            self.order(self.sids[0], self._cfg['sell_amount'])
                            self.invested_sell = False
                            self.buy = True

                    # save to recorder
                    signals = {
                        'open': open[-1],
                        'high': high[-1],
                        'low': low[-1],
                        'close': close[-1],
                        'volume': volume[-1],
                        'buy': self.buy,
                        'sell': self.sell
                    }
                    self.record(**signals)

# register to alg tasks
AlgRegister.add(Kmeans)

def run(opt='twse', debug=False, limit=0):
    maxlen = 30
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    report = Report(
        'kmeans',
        sort=[('buys', False), ('sells', False), ('portfolio_value', False)], limit=20)
    # set debug or normal mode
    kwargs = {
        'debug': debug,
        'limit': limit,
        'opt': opt
    }
    idhandler = TwseIdDBHandler(**kwargs) if kwargs['opt'] == 'twse' else OtcIdDBHandler(**kwargs)
    for stockid in idhandler.stock.get_ids():
        try:
            kwargs = {
                'opt': opt,
                'targets': ['stock'],
                'starttime': starttime,
                'endtime': endtime,
                'stockids': [stockid],
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

            kmeans = Kmeans(dbhandler=dbhandler, debug=True, sim_params=sim_params)
            results = kmeans.run(panel).fillna(0)
            risks = kmeans.perf_tracker.handle_simulation_end()  
            report.collect(stockid, results, risks)
            print "%s pass" %(stockid)
        except:
            print traceback.format_exc()
            continue

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'kmeans.html')

    for stockid in report.iter_symbol():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "kmeans_%s.html" % (stockid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test kmeans algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store', type=str, default='twse', help='twse/otc')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    #proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    #close_main_service(proc, args.debug)
