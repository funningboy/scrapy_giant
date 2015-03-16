# -*- coding: utf-8 -*-

import pytz

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

# Import exponential moving average from talib wrapper
from zipline.transforms.ta import OBV, AD

from datetime import datetime, timedelta

from bin.mongodb_driver import *
from bin.start import *
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler

from algorithm.report import Report

class ZombieAlgorithm(TradingAlgorithm):
    """
    This algorithm use strong buy/sell signals following by topbuy/
    topsell info, if topbuy's volume >= stockid.volume * 10 % then buy a count,
    after checking topsell's volume >= stockid.volume * 10 % then sell a count if shared has count
    """

    def __init__(self, dbhandler, *args, **kwargs):
        super(ZombieAlgorithm, self).__init__(*args, **kwargs)
        self.dbhandler = dbhandler
        self.mstockid = self.dbhandler.stock.ids[0]

    def initialize(self, ema_window=10):
        # To keep track of whether we invested in the stock or not
        # pool checkpoint
        self.invested = False
        self.idxmin = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.idxmax = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.idxcur = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.idxbuy = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.idxsell = (pytz.timezone('UTC').localize(datetime.utcnow()), -1, -1)
        self.real_obv_trans = OBV()
        self.real_ad_trans = AD()

    def handle_data(self, data):
        self.real_obv = self.real_obv_trans.handle_data(data)
        self.real_ad = self.real_ad_trans.handle_data(data)
        if self.real_obv is None or self.real_ad is None:
            return

        # minidx
        if self.idxmin[1] == -1:
            self.idxmin = (data[self.mstockid].dt, data[self.mstockid].price, data[self.mstockid].volume)
        else:
            if data[self.mstockid].price <= self.idxmin[1]:
                self.idxmin = (data[self.mstockid].dt, data[self.mstockid].price, data[self.mstockid].volume)

        # maxidx
        if self.idxmax[1] == -1:
            self.idxmax = (data[self.mstockid].dt, data[self.mstockid].price, data[self.mstockid].volume)
        else:
            if data[self.mstockid].price >= self.idxmax[1]:
                self.idxmax = (data[self.mstockid].dt, data[self.mstockid].price, data[self.mstockid].volume)

        # curidx
        self.idxcur = (data[self.mstockid].dt, data[self.mstockid].price, data[self.mstockid].volume)

        self.buy = False
        self.sell = False

        #buyrule
        self.buy = self.idxmax[0] <= self.idxmin[0] - timedelta(days=40) and \
        self.idxcur[0] >= self.idxmin[0] + timedelta(days=1) and \
        data[self.mstockid].close < data[self.mstockid].open * 1.01 and \
        data[self.mstockid].close >= data[self.mstockid].open

        #sellrule
        if self.invested:
            self.sell = self.idxcur[0] >= self.idxbuy[0] + timedelta(5)

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

        # save to recorder
        signals = {
            'open': data[self.mstockid].open,
            'high': data[self.mstockid].high,
            'low': data[self.mstockid].low,
            'close': data[self.mstockid].close,
            'volume': data[self.mstockid].volume,
            'obv': self.real_obv[self.mstockid],
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
    # set time window
    starttime = datetime.utcnow() - timedelta(days=300)
    endtime = datetime.utcnow()
    report = Report(
        algname=ZombieAlgorithm.__name__,
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
        try:
            data = dbhandler.transform_all_data(starttime, endtime, [stockid], [], 'totalvolume', 10)
            zombie = ZombieAlgorithm(dbhandler=dbhandler)
            results = zombie.run(data).fillna(0)
            report.collect(stockid, results)
            print "%s" %(stockid)
        except:
            continue

    if report.report.empty:
        return

    # report summary
    stream = report.summary(dtype='html')
    report.write(stream, 'zombie.html')

    for stockid in report.iter_stockid():
        stream = report.iter_report(stockid, dtype='html')
        report.write(stream, "zombie_%s.html" % (stockid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test zombie algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('--random', dest='random', action='store_true', help='random')
    parser.add_argument('--limit', dest='limit', action='store', type=int, default=0, help='limit')
    args = parser.parse_args()
    #proc = start_main_service(args.debug)
    proc = start_main_service(True)
    run('twse', args.debug, args.limit)
    close_main_service(proc, args.debug)
