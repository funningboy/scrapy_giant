# -*- coding: utf-8 -*-

from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.tasks import query_hisstock, query_histoptrader
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler

# handler tasks sync
hisdb_tasks = {
    'twse': TwseHisDBHandler,
    'otc': OtcHisDBHandler
}

iddb_tasks = {
    'twse': TwseIdDBHandler,
    'otc': OtcIdDBHandler
}

def hisstock_list(request, hisdb, endtime, order='totalvolume', limit=10):
    """ list all stocks
    """
    dbhandler = hisdb_tasks[hisdb]()
    idhandler = iddb_tasks[hisdb]()
    end_yy, end_mm, end_dd = int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8])
    endtime = datetime(end_yy, end_mm, end_dd)
    stockids =[id for id in idhandler.stock.get_ids()]
    args = (endtime, endtime, stockids, order, limit)
    stockitem = dbhandler.stock.query(*args)
    return render(request,'handler/stocklist.html', {'stockitem': stockitem})

def hisstock_detail(request, hisdb, stockid, starttime, endtime,
                    traderids=[], order='totalvolume', limit=10):
    """ show stock detail
    """
    dbhandler = hisdb_tasks[hisdb]()
    start_yy, start_mm, start_dd = int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8])
    end_yy, end_mm, end_dd = int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8])
    starttime, endtime = datetime(start_yy, start_mm, start_dd), datetime(end_yy, end_mm, end_dd)
    args = (starttime, endtime, [stockid], order, limit)
    stockitem = dbhandler.stock.query(*args)
    args = (starttime, endtime, [stockid], traderids, 'stock', order, limit)
    traderitem = dbhandler.trader.query(*args)
    return render(request,'handler/stockdetail.html', {'stockitem': stockitem, 'traderitem': traderitem})

def histrader_list(request, hisdb, endtime, order='totalvolume', limit=10):
    """ list all traders
    """
    dbhandler = hisdb_tasks[hisdb]()
    idhandler = iddb_tasks[hisdb]()
    endtime = datetime(end_yy, end_mm, end_dd)
    traderids = [id for id in idhandler.trader.get_ids()]
    args = (endtime, endtime, [], traderids, 'trader', order, limit)
    traderitem = dbhandler.trader.query(*args)
    return render(request,'handler/traderlist.html', {'traderitem': traderitem})

def histrader_detail(request, hisdb, traderid, starttime, endtime,
                     stockids=[], order='totalvolume', limit=10):
    """ show trader detail
    """
    dbhandler = hisdb_tasks[hisdb]()
    start_yy, start_mm, start_dd = int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8])
    end_yy, end_mm, end_dd = int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8])
    starttime, endtime = datetime(start_yy, start_mm, start_dd), datetime(end_yy, end_mm, end_dd)
    args = (starttime, endtime, stockids, [traderid], 'trader', order, limit)
    traderitem = dbhandler.trader.query(*args)
    stockids = [it.stockid for it in traderitem]
    args = (starttime, endtime, stockids, order, limit)
    stockitem = dbhandler.stock.query(*args)
    return render(request,'handler/traderdetail.html', {'stockitem': stockitem, 'traderitem': traderitem})
