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
    https://www.quantopian.com/posts/inferring-latent-states-using-a-gaussian-hidden-markov-model
    bear market: smaller mean, higher variant
    bull market: higher mean, smaller variant
    """

    def __init__(self, dbhandler, *args, **kwargs):
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids
        self.n_components = int(kwargs.pop('n_components')) or 5
        self.n_iter = int(kwargs.pop('n_iter')) or 1000

    def run(self, data):
        sid = self.sids[0]
        self.dates = data[sid]['price'].values
        self.close_v = data[sid]['close_v'].values
        self.volume = data[sid]['volume'].values[1:]

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
    report = Report(
        sort=[('buys', False), ('sells', False), ('portfolio_value', False)], limit=20)
    kwargs = {
        'debug': debug,
        'limit': limit,
        'opt': opt
    }
    idhandler = TwseIdDBHandler() if kwargs['opt'] == 'twse' else OtcIdDBHandler()
    for stockid in idhandler.stock.get_ids(**kwargs):
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

            hmm = GaussianHmmLib(dbhandler=dbhandler, debug=debug, sim_params=sim_params)
            results = hmm.run(panel).fillna(0)
            risks = hmm.perf_tracker.handle_simuulation_end()
            report.collect(stockid, results, risks)
            print "%s pass" %(stockid)
        except:
            print traceback.format_exc()
            continue

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'gaussianhmm.html')

    for stockid in report.iter_symbol():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "gaussianhmm_%s.html" % (stockid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='train GaussianHmm algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store_true', help='twse/otc')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    #proc = start_main_service(args.debug)
    run(args.opt, args.debug, args.limit)
    #close_main_service(proc, args.debug)
