# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import numpy as np
import pylab as pl
import pytz
import matplotlib.pyplot as plt

from sklearn import neighbors

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from bin.mongodb_driver import *
from bin.start import *
from query.hisdb_query import *
from query.iddb_query import *
from algorithm.report import Report


class kdtKnnAlgorithm(TradingAlgorithm):
    """
    ref: http://wiki.quantsoftware.org/index.php?title=Gallery
         https://github.com/QuantSoftware/QuantSoftwareToolkit/blob/master/QSTK/qstklearn/kdtknn.py
    """

    def __init__(self, dbhandler, **kwargs):
        super(KdtKnnAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids
        self.dbhandler.credit.ids
        self.dbhandler.future.ids

    def initialize(self):
        pass

    def handle_data(self, data):
        pass


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    maxlen = 30
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    report = Report(
        sort=[('buy_count', False), ('sell_count', False), ('volume', False)], limit=20)

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
                'traderids': [],
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

            kdtree = kdtKnnAlgorithm(dbhandler=dbhandler, sim_params=sim_params)
            results = kdtree.run(data).fillna(0)
            risks = kdtree.perf_tracker.handle_simulation_end()
            report.collect(stockid, results, risks)
            print "%s pass" %(stockid)
    except:
        print traceback.format_exc()
        continue

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'kdtknn.html')

    for stockid in report.iter_stockid():
        stream = report.iter_report(stockid, dtype='html', has_other=True, has_sideband=True)
        report.write(stream, "kdtknn_%s.html" % (stockid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test superman algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--opt', dest='opt', action='store_true', default='twse', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
#    proc = start_main_service(args.debug)
    proc = start_main_service(True)
    run(args.opt, args.debug, args.limit)
    close_main_service(proc, args.debug)
