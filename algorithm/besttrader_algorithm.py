# -*- coding: utf-8 -*-

import pytz
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from sklearn import cluster, covariance, manifold

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from datetime import datetime, timedelta

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from algorithm.report import Report


class BestTraderAlgorithm(TradingAlgorithm):
    """
    find the best correlation between trader and stocks
    ref: http://scikit-learn.org/stable/auto_examples/applications/plot_stock_market.html
    https://www.quantopian.com/posts/working-with-history-dataframes
    """

    def __init__(self, dbhandler, *args, **kwargs):
        super(BestTraderAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.sids = self.dbhandler.stock.ids
        self.tids = self.dbhandler.trader.ids

    def initialize(self):
        self.edge_model = covariance.GraphLassoCV()
        self.window = deque(max_len=70)
        self.X =
        self.Y =

    def handle_data(self, data):
        data[self.sids[0]].top0_buyvolume
        data[self.sids[0]].top0_sellvolume
        data[self.sids[0]].top0_price

        # save to recorder
        signals = {
            'open': data[self.sids[0]].open,
            'high': data[self.sids[0]].high,
            'low': data[self.sids[0]].low,
            'close': data[self.sids[0]].close,
            'volume': data[self.sids[0]].volume,
        }

        # map sideband signal
        try:
            alias_top0 = self.dbhandler.trader.map_alias([self.sids[0]], 'stock', ['top0'])[0]
            signals.update({
                "topbuy0_%s" % (alias_topbuy0): data[self.sids[0]].topbuy0,
            })
        except:
            pass
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
    traderid = '1590'
    idhandler = TwseIdDBHandler() if kwargs['opt'] == 'twse' else OtcIdDBHandler()
    for stockid in idhandler.stock.get_ids(**kwargs):
        dbhandler = TwseHisDBHandler() if kwargs['opt'] == 'twse' else OtcHisDBHandler()
        dbhandler.stock.ids = [stockid]
        data = dbhandler.transform_all_data(starttime, endtime, [stockid], [traderid], 'totalvolume', 10)
        besttrader = BestTraderAlgorithm(dbhandler=dbhandler)
        results = besttrader.run(data).fillna(0)
        report.collect(stockid, results)
        print "%s pass" %(stockid)

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
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
#    proc = start_main_service(args.debug)
    proc = start_main_service(True)
    run('twse', args.debug, args.limit)
    close_main_service(proc, args.debug)
