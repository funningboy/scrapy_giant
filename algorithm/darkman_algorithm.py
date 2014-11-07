# -*- coding: utf-8 -*-

import pytz

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

from datetime import datetime, timedelta

from bin.mongodb_driver import *
from bin.start import *
from query.hisdb_query import *
from query.iddb_query import *
from algorithm.report import Report


class DarkManAlgorithm(TradingAlgorithm):
    """
    follow the specified trader record
    """

    def __init__(self, dbquery, *args, **kwargs):
        super(DarkManAlgorithm, self).__init__(*args, **kwargs)
        self.dbquery = dbquery
        self.mstockid = self.dbquery._stockmap.keys()[0]

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
            signals.update({
                'topbuy0_%s' % (self.dbquery.find_stockmap(self.mstockid, 'topbuy0')): data[self.mstockid].topbuy0,
                'topsell0_%s' % (self.dbquery.find_stockmap(self.mstockid, 'topsell0')): data[self.mstockid].topsell0
            })
        except:
          pass
        self.record(**signals)


def main(debug=False, limit=0):
    proc = start_service(debug)
    # set time window
    starttime = datetime.utcnow() - timedelta(days=30)
    endtime = datetime.utcnow()

    # set debug or normal mode
    kwargs = {
        'debug': debug,
        'limit': limit
    }
    # query topbuylist by each trader
    # 1590:u'花旗環球', 1440:u'美林'
    for traderid in TraderIdDBQuery().get_traderids(**kwargs):
        dbquery = TwseHisDBQuery()
        topdt = dbquery.get_toptrader_data(
            starttime=starttime,
            endtime=endtime,
            traderids=[traderid],
            opt='trader',
            dtyp='buy',
            limit=10
        )
        report = Report(
            algname=DarkManAlgorithm.__name__,
            sort=[('buy_count', -1), ('sell_count', -1), ('ending_value', -1), ('close', -1)], limit=20)
        kwargs = {
            'debug': debug,
            'limit': limit
        }
        stockids = [dbquery.find_tradermap(traderid, 'topbuy%d' % (i)) for i in range(5)]
        for stockid in stockids:
            dbquery = TwseHisDBQuery()
            data = dbquery.get_all_data(
                starttime=starttime,
                endtime=endtime,
                traderids=[traderid],
                stockids=[stockid])
            if data.empty:
                continue
            darkman = DarkManAlgorithm(dbquery=dbquery)
            results = darkman.run(data).fillna(0)
            if results.empty:
                continue
            report.collect(stockid, results)
            print traderid, stockid

        # report summary
        stream = report.summary(dtype='html')
        report.write(stream, 'darkman_%s.html' % (traderid))

        for stockid in report.iter_stockid():
            stream = report.iter_report(stockid, dtype='html')
            report.write(stream, "darkman_%s_%s.html" % (traderid, stockid))

    close_service(proc, debug)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test darkman algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', help='debug mode')
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    main(debug=True if args.debug else False, limit=args.limit)
