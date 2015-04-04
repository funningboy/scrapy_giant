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
        self.sids = self.dbhandler.stock.ids
        self.leafsize = int(kwargs.pop('leafsize')) or 10
        self.k = int(kwargs.pop('k')) or 3

    def initialize(self):

    def handle_data(self, data):

    def post_run(self):
        knn = neighbors.KNeighborsClassifier()
        knn.fit(train.data, train.target)
        knn.score(test.data, test.target)


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    # set time window
    starttime = datetime.utcnow() - timedelta(days=300)
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
    idhandler = TwseIdDBHandler() if kwargs['opt'] == 'twse' else OtcIdDBHandler()
    for stockid in idhandler.stock.get_ids(**kwargs):
        dbhandler = TwseHisDBHandler() if kwargs['opt'] == 'twse' else OtcHisDBHandler()
        dbhandler.stock.ids = [stockid]
        data = dbhandler.transform_all_data(starttime, endtime, [stockid], [], 'totalvolume', 10)
        supman = SuperManAlgorithm(dbhandler=dbhandler)
        results = supman.run(data).fillna(0)
        report.collect(stockid, results)
        print "%s pass" %(stockid)

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
