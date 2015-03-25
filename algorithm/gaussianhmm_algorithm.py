# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import numpy as np
import pytz
import matplotlib.pyplot as plt

from sklearn.hmm import GaussianHMM

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from algorithm.report import Report


class GaussianHmmLib:
    """
    ref: http://scikit-learn.org/0.14/auto_examples/applications/plot_hmm_stock_analysis.html
    bear market: smaller mean, higher variant
    bull market: higher mean, smaller variant
    """

    def __init__(self, dbhandler, *args, **kwargs):
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids
        self.n_components = int(kwargs.pop('n_components')) or 5
        self.n_iter = int(kwargs.pop('n_iter')) or 1000

    def run(self, data):
        self.dates = data[self.sids[0]]['price'].values
        self.close_v = data[self.sids[0]]['close_v'].values
        self.volume = data[self.sids[0]]['volume'].values[1:]

        # take diff of close value
        # this makes len(diff) = len(close_t) - 1
        # therefore, others quantity also need to be shifted
        self.diff = self.close_v[1:] - self.close_v[:-1]

        # pack diff and volume for training
        self.X = np.column_stack([self.diff, self.volume])

        # make an HMM instance and execute fit
        self.model = GaussianHMM(self.n_components, covariance_type="diag", n_iter=self.n_iter)
        self.model.fit([self.X], n_iter=self.n_iter)

        # predict the optimal sequence of internal hidden state
        self.hidden_states = self.model.predict(self.X)

    def report(self):
        # print trained parameters and plot
        print "Transition matrix"
        print self.model.transmat_
        print ""

        print "means and vars of each hidden state"
        for i in xrange(self.n_components):
            print "%dth hidden state" % i
            print "mean = ", self.model.means_[i]
            print "var = ", np.diag(self.model.covars_[i])
            print ""

        years = YearLocator()   # every year
        months = MonthLocator()  # every month
        yearsFmt = DateFormatter('%Y')
        fig = plt.figure()
        ax = fig.add_subplot(111)

        for i in xrange(self.n_components):
            # use fancy indexing to plot data in each state
            idx = (self.hidden_states == i)
            ax.plot_date(self.dates[idx], self.close_v[idx], 'o', label="%dth hidden state" % i)
        ax.legend()

        # format the ticks
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        ax.autoscale_view()

        # format the coords message box
        ax.fmt_xdata = DateFormatter('%Y-%m-%d')
        ax.fmt_ydata = lambda x: '$%1.2f' % x
        ax.grid(True)

        fig.autofmt_xdate()
        plt.savefig("gaussianhmm_%s.png" %(self.sids[0]))
#        plt.show()


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    # set time window
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
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
        hmm = GaussianHmmLib(dbhandler=dbhandler)
        hmm.run(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='train GaussianHmm algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store_true', help='twse/otc')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    close_main_service(proc, args.debug)
