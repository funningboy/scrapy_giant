# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.tasks import *

def test(request):
    return render(request, 'handler/dualema_1314.html')

def search_form(request):
    return render(request, 'handler/search_form.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        starttime = datetime.utcnow() - timedelta(days=4)
        endtime = datetime.utcnow() - timedelta(days=2)
        args = (starttime, endtime, ['2317'])
        stockitem = hisdb_tasks('twse').stock.query(*args)
        data = {'name': 'sean'}
        return render(request, 'handler/search_results.html',
                      {'stockitem': stockitem, 'data': data, 'query': q})
    else:
        return render(request, 'handler/search_form.html', {'error': True})

def hisstock_list(request, opt, starttime, endtime, order='totalvolume', limit=100):
    dbhandler = hisdb_tasks[opt]()
    idhandler = iddb_tasks[opt]()
    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    stockids =[id for id in idhandler.stock.get_ids()]
    args = (starttime, endtime, stockids, order, limit)
    stockitem = dbhandler.stock.query(*args)
    return render(request,'handler/hisstock_list.html', {'stockitem': stockitem})

def hisstock_detail(request, opt, stockid, starttime, endtime, traderids=[], order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[opt]()
    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    args = (starttime, endtime, [stockid], order, limit)
    stockitem = dbhandler.stock.query(*args)
    args = (starttime, endtime, [stockid], traderids, 'stock', order, limit)
    traderitem = dbhandler.trader.query(*args)
    return render(request,'handler/hisstock_detail.html', {'stockitem': stockitem, 'traderitem': traderitem})

def histrader_list(request, opt, starttime, endtime, order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[opt]()
    idhandler = iddb_tasks[opt]()
    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    traderids = [id for id in idhandler.trader.get_ids()]
    args = (starttime, endtime, [], traderids, 'trader', order, limit)
    traderitem = dbhandler.trader.query(*args)
    return render(request,'handler/histrader_list.html', {'traderitem': traderitem})

def histrader_detail(request, opt, traderid, starttime, endtime, stockids=[], order='totalvolume', limit=10):
    dbhandler = hisdb_tasks[opt]()
    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    args = (starttime, endtime, stockids, [traderid], 'trader', order, limit)
    traderitem = dbhandler.trader.query(*args)
    stockids = [it.stockid for it in traderitem]
    args = (starttime, endtime, stockids, order, limit)
    stockitem = dbhandler.stock.query(*args)
    return render(request,'handler/histrader_detail.html', {'stockitem': stockitem, 'traderitem': traderitem})
