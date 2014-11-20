# -*- coding: utf-8 -*-

import pytz

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from datetime import datetime, timedelta

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from algorithm.report import Report


class DarkManAlgorithm(TradingAlgorithm):
    """
    follow the specified trader record
    """

    def __init__(self, dbhandler, *args, **kwargs):
        super(DarkManAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        # main stockid, no reference stockids
        self.mstockid = self.dbhandler.stock.ids[0]

    def initialize(self):
        self.invested = False
        self.idxbuy = (pytz.timezone('UTC').localize(datetime.utcnow()), -1)
        self.idxsell = (pytz.timezone('UTC').localize(datetime.utcnow()), -1)

    def handle_data(self, data):
        self.buy = False
        self.sell = False

        # sell after buy
        self.buy = data[self.mstockid].topbuy0 > 100

        if self.invested:
            self.sell = data[self.mstockid].dt >= self.idxbuy[0] + timedelta(1)

        if self.buy and not self.invested:
            self.order(self.mstockid, 1000)
            self.invested = True
            self.buy = True
            self.sell = False
            self.idxbuy = (data[self.mstockid].dt, data[self.mstockid].price)
        elif self.sell and self.invested:
            self.order(self.mstockid, -1000)
            self.invested = False
            self.buy = False
            self.sell = True
            self.idxsell = (data[self.mstockid].dt, data[self.mstockid].price)

        # save to recorder
        signals = {
            'open': data[self.mstockid].open,
            'high': data[self.mstockid].high,
            'low': data[self.mstockid].low,
            'close': data[self.mstockid].close,
            'volume': data[self.mstockid].volume,
            'buy': self.buy,
            'sell': self.sell
        }

        # add sideband signal
        try:
            alias_topbuy0 = self.dbhandler.trader.map_alias([self.mstockid], 'stock', ['topbuy0'])[0]
            alias_topsell0 = self.dbhandler.trader.map_alias([self.mstockid], 'stock', ['topsell0'])[0]
            signals.update({
                'topbuy0_%s' % (alias_topbuy0): data[self.mstockid].topbuy0,
                'topsell0_%s' % (alias_topsell0): data[self.mstockid].topsell0
            })
        except:
            pass
        self.record(**signals)


def run(opt='twse', debug=False, limit=0):
    """ as doctest run """
    # set time window
    starttime = datetime.utcnow() - timedelta(days=30)
    endtime = datetime.utcnow()

    # set debug or normal mode
    kwargs = {
        'debug': debug,
        'limit': limit,
        'opt': opt
    }
    # query topbuylist by each trader
    # 1590:u'花旗環球', 1440:u'美林'
    idhandler = TwseIdDBHandler() if kwargs['opt'] == 'twse' else OtcIdDBHandler()
    for traderid in idhandler.trader.get_ids(**kwargs):
        dbhandler = TwseHisdbhandler() if kwargs['opt'] == 'twse' else OtcHisDBHandler()
        topdt = dbhandler.trader.gettoptrader_data(starttime, endtime, [traderid], 'trader', 'buy', 10)
        report = Report(
            algname=DarkManAlgorithm.__name__,
            sort=[('buy_count', -1), ('sell_count', -1), ('ending_value', -1), ('close', -1)], limit=20)
        kwargs = {
            'debug': debug,
            'limit': limit,
            'opt': opt
        }
        stockids = dbhandler.trader.map_alias([traderid], 'trader', ['topbuy%d' % (i) for i in range(5)])
        for stockid in stockids:
            dbhandler = TwseHisdbhandler() if kwargs['opt'] == 'twse' else OtcHisDBHandler()
            data = dbhandler.transform_all_data(starttime, endtime, [traderid], [stockid], 10)
            if data.empty:
                continue
            darkman = DarkManAlgorithm(dbhandler=dbhandler)
            results = darkman.run(data).fillna(0)
            if results.empty:
                continue
            report.collect(stockid, results)
            print traderid, stockid

        # report summary
        stream = report.summary(dtype='html')
        report.write(stream, 'darkman_%s.html' % (traderid))

        for stockid in report.iter_stockid():
            stream = report.iter_report(stockid, dtype='html', has_other=True, has_sideband=True)
            report.write(stream, "darkman_%s_%s.html" % (traderid, stockid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test darkman algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    proc = start_main_service(args.debug)
    run('twse', args.debug, args.limit)
    close_main_service(proc, args.debug)
