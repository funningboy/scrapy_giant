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

    def __init__(self, dbhandler, *args, **kwargs):
        super(KdtKnnAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        # main stockid, no reference stockids
        self.mstockid = self.dbhandler.stock.ids[0]

    def initialize(self):

    def handle_data(self, data):
        data[self.mstockid].price -
        data[self.mstockid].dt

    def post_run(self):
        knn = neighbors.KNeighborsClassifier()
        knn.fit(train.data, train.target)
        knn.score(test.data, test.target)

        pass

def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    # set time window
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    # sort factor
    report = Report(
        algname=SuperManAlgorithm.__name__,
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
        supman = SuperManAlgorithm(dbhandler=dbhandler)
        results = supman.run(data).fillna(0)
        if results.empty:
            continue
        report.collect(stockid, results)
        print stockid

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'superman.html')

    for stockid in report.iter_stockid():
        stream = report.iter_report(stockid, dtype='html', has_other=True, has_sideband=True)
        report.write(stream, "superman_%s.html" % (stockid))


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
