# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from zipline.algorithm import TradingAlgorithm
from zipline.utils.factory import *

class DarkManAlgorithm(TradingAlgorithm):
    """
    follow the specified trader record
    """

    def __init__(self, dbquery, *args, **kwargs):
        super(DarkManAlgorithm, self).__init__(*args, **kwargs)
        self.dbquery = dbquery
        self.mstockid = self.dbquery._stockmap.keys()[0]

    def initialize(self):
        pass

def mian(debug):
    proc = start_service()
    # set time window
    starttime = datetime.utcnow() - timedelta(days=60)
    endtime = datetime.utcnow()
    report = Report(
        algname=DarkManAlgorithm.__name__,
        sort=[('ending_value', -1), ('close', -1)], limit=20)

    # set debug or normal mode
    kwargs = {
        'debug': False,
        'limit': 0
    }
    # specified trader ids
    traderids = ['', '']
    dbquery = TwseHisDBQuery()
    # 1. find trader buy/sell list as stockid
    data = dbquery.get_all_data(
        starttime=starttime, endtime=endtime,
        stockids=[], traderids=traderids)
#    if data.empty:
#        continue
    # 2. remap stockid to requery
#    for data
#    darkman = DarkManAlgorithm(dbquery=dbquery)
#    results = darkman.run(data).dropna()
#    report.collect(stockid, results)
#
#    stream = report.summary(dtype='html')
#    report.write(stream, 'darkman_%s.html')

    close_service(proc, debug)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test darkman algorithm')
    parser.add_argument('--debug', dest='debug', action='store_true', help='debug mode')
    args = parser.parse_args()
    main(debug=True if args.debug else False)
