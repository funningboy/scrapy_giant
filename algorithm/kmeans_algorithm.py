# -*- coding: utf-8 -*-

import pytz
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import deque

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from algorithm.report import Report


class KmeansAlgorithm(TradingAlgorithm):

    def __init__(self, dbhandler, *args, **kwargs):
        super(KmeansAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids

    def initialize(self):
        self.window = deque(maxlen=70)
        self.X = deque(maxlen=200)
        self.Y = deque(maxlen=200)

    def _bench_k_means(self, estimator, name, train):
        t0 = time()
        estimator.fit(train)
        print('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
              % (name, (time() - t0), estimator.inertia_,
                 metrics.homogeneity_score(labels, estimator.labels_),
                 metrics.completeness_score(labels, estimator.labels_),
                 metrics.v_measure_score(labels, estimator.labels_),
                 metrics.adjusted_rand_score(labels, estimator.labels_),
                 metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
                 metrics.silhouette_score(train, estimator.labels_,
                                          metric='euclidean',
                                          sample_size=sample_size)))

    def _classifier(self, train):
        self._bench_k_means(KMeans(init='k-means++', n_clusters=5, n_init=10),
                          name="k-means++", train=train)

        self._bench_k_means(KMeans(init='random', n_clusters=5, n_init=10),
                          name="random", train=train)

        # in this case the seeding of the centers is deterministic, hence we run the
        # kmeans algorithm only once with n_init=1
        pca = PCA(n_components=5).fit(train)
        self._bench_k_means(KMeans(init=pca.components_, n_clusters=5, n_init=1),
                      name="PCA-based",
                      train=train)
        print(79 * '_')

        ###############################################################################
        # Visualize the results on PCA-reduced data

        reduced_data = PCA(n_components=2).fit_transform(train)
        kmeans = KMeans(init='k-means++', n_clusters=5, n_init=10)
        kmeans.fit(reduced_data)

        # Step size of the mesh. Decrease to increase the quality of the VQ.
        h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

        # Plot the decision boundary. For that, we will assign a color to each
        x_min, x_max = reduced_data[:, 0].min() + 1, reduced_data[:, 0].max() - 1
        y_min, y_max = reduced_data[:, 1].min() + 1, reduced_data[:, 1].max() - 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Obtain labels for each point in mesh. Use last trained model.
        Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

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
        plt.show()

    def handle_data(self, data):
        print data[self.mstockid].price
        self.window.append(data[self.mstockid].price)

        if len(self.window) == 70:
            self.changes = np.diff(self.window) > 0
            self.X.append(self.changes[:-1])
            self.Y.append(self.changes[-1])

            if len(self.Y) >= 100:
                self._classifier(train=[self.X, self.Y])

def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    # set time window
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    # sort factor
    report = Report(
        algname=KmeansAlgorithm.__name__,
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
        supman = KmeansAlgorithm(dbhandler=dbhandler)
        results = supman.run(data).fillna(0)
        #report.collect(stockid, results)
        print "%s" %(stockid)

#    if report.report.empty:
#        return
#
#    # report summary
#    stream = report.summary(dtype='html')
#    report.write(stream, 'superman.html')
#
#    for stockid in report.iter_stockid
#        stream = report.iter_report(stockid, dtype='html', has_other=True, has_sideband=True)
#        report.write(stream, "superman_%s.html" % (stockid))
#
#    for stockid in report.iter_stockid():
#        fig = plt.figure()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test superman algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
#    proc = start_main_service(args.debug)
    proc = start_main_service(True)
    run('twse', args.debug, args.limit)
    close_main_service(proc, args.debug)
