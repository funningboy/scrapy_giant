# -*- coding: utf-8 -*-

from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.tasks import query_hisstock, query_histoptrader
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler
from handler.tasks import *


def hisstock_list(request, hisdb, starttime, endtime, order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[hisdb]()
    idhandler = iddb_tasks[hisdb]()
    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    stockids =[id for id in idhandler.stock.get_ids()]
    args = (starttime, endtime, stockids, order, limit)
    stockitem = dbhandler.stock.query(*args)
    return render(request,'handler/hisstock_list.html', {'stockitem': stockitem})

def hisstock_detail(request, hisdb, stockid, starttime, endtime, traderids=[], order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[hisdb]()
    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    args = (starttime, endtime, [stockid], order, limit)
    stockitem = dbhandler.stock.query(*args)
    args = (starttime, endtime, [stockid], traderids, 'stock', order, limit)
    traderitem = dbhandler.trader.query(*args)
    return render(request,'handler/hisstock_detail.html', {'stockitem': stockitem, 'traderitem': traderitem})

def histrader_list(request, hisdb, starttime, endtime, order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[hisdb]()
    idhandler = iddb_tasks[hisdb]()
    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    traderids = [id for id in idhandler.trader.get_ids()]
    args = (starttime, endtime, [], traderids, 'trader', order, limit)
    traderitem = dbhandler.trader.query(*args)
    return render(request,'handler/histrader_list.html', {'traderitem': traderitem})

def histrader_detail(request, hisdb, traderid, starttime, endtime, stockids=[], order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[hisdb]()
    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    args = (starttime, endtime, stockids, [traderid], 'trader', order, limit)
    traderitem = dbhandler.trader.query(*args)
    stockids = [it.stockid for it in traderitem]
    args = (starttime, endtime, stockids, order, limit)
    stockitem = dbhandler.stock.query(*args)
    return render(request,'handler/histrader_detail.html', {'stockitem': stockitem, 'traderitem': traderitem})
