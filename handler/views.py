# -*- coding: utf-8 -*-

from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.models import TwseHisColl, OtcHisColl
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler

hisdb_tasks = {
    'twse': TwseHisDBHandler,
    'otc': OtcHisDBHandler
}

iddb_tasks = {
    'twse': TwseIdDBHandler,
    'otc': OtcIdDBHandler
}

def hisstock_list(request, hisdb):
    """ list all stocks
    """
    pass

def hisstock_detail(request, hisdb, stockid, starttime, endtime,
                    traderids=[], order='totalvolume', limit=10):
    """ show stock
    """
    dbhandler = hisdb_tasks[hisdb]()
    idhandler = iddb_tasks[hisdb]()
    start_yy, start_mm, start_dd = int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8])
    end_yy, end_mm, end_dd = int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8])
    stockitem = query_hisstock()
    traderitem = query_histoptrader()
    return render(request,'handler/stockdetail.html', {'stockitem': stockitem, 'traderitem': traderitem})

def histrader_list(request):
    pass

def histrader_detail(request, hisdb, traderid, starttime, endtime,
                     stockids=[], order='totalvolume', limit=10):
    """ show trader detail
    """
    dbhandler = hisdb_tasks[hisdb]()
    idhandler = iddb_tasks[hisdb]()
    start_yy, start_mm, start_dd = int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8])
    end_yy, end_mm, end_dd = int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8])
    # 1st
    traderitem = dbhandler.trader.query(
        starttime=datetime(start_yy, start_mm, start_dd),
        endtime=datetime(end_yy, end_mm, end_dd),
        stockids=stockids,
        traderids=[traderid],
        base='trader',
        order=order,
        limit=limit)
    stockids = [it.stockid for it in traderitem]
    # 2nd
    stockitem = dbhandler.stock.query(
        starttime=datetime(start_yy, start_mm, start_dd),
        endtime=datetime(end_yy, end_mm, end_dd),
        stockids=stockids)
    return render(request,'handler/traderdetail.html', {'stockitem': stockitem, 'traderitem': traderitem})
