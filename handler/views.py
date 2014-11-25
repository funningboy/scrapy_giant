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

def hisstock_list(request):
    return render(request,'handler/stockAddRemovePanel2.html', {})

def hisstock_detail(request, hisdb, stockid, starttime, endtime, traderid=None, base='stock', order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[hisdb]()
    idhandler = iddb_tasks[hisdb]()
    dbhandler.stock.ids = [stockid] if idhandler.stock.has_id(stockid) else []
    dbhandler.trader.ids = [traderid] if idhandler.trader.has_id(traderid) else []
    start_yy, start_mm, start_dd = int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8])
    end_yy, end_mm, end_dd = int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8])
    stockitem = dbhandler.stock.query(
        starttime=datetime(start_yy, start_mm, start_dd),
        endtime=datetime(end_yy, end_mm, end_dd),
        stockids=[stockid])
    traderitem = dbhandler.trader.query(
        starttime=datetime(start_yy, start_mm, start_dd),
        endtime=datetime(end_yy, end_mm, end_dd),
        stockids=[stockid],
        traderids=[traderid],
        base=base,
        order=order,
        limit=limit)
    return render(request,'handler/stockdetail.html', {'stockitem': stockitem, 'traderitem': traderitem})

def histrader_detail(request, hisdb, stockid, traderid, starttime, endtime, base='trader', order='totalvolume', limit=10):
    pass

def histrader_list()
    pass
