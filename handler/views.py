# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from handler.tasks import *
from handler.group import *

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

#def get_hisstock_list(request, opt, starttime, endtime, order='totalvolume', limit=100):
#    try:
#        if request.method == 'GET':
#            kwargs = {}
#            dbhandler = hisdb_tasks[opt]()
#            kwargs = {}
#            idhandler = iddb_tasks[opt]()
#            starttime = datetime(mapint(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
#            endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
#            stockids =[id for id in idhandler.stock.get_ids()]
#            args = (starttime, endtime, stockids, order, limit)
#            stockitem = dbhandler.stock.query_raw(*args)
#            return render(request,'handler/hisstock_list.html', {'stockitem': stockitem})
#    except:
#
#
#def get_hisstock_list_json

def get_hisstock_detail(request, opt, stockid, starttime, endtime, traderids=None, order='totalvolume', limit=10):
    try:
        if request.method == 'GET':
            return render(request,'handler/hisstock_detail.html')
    except:
        return HttpResponse(404)

def get_hisstock_detail_json(request, opt, stockid, starttime, endtime, traderids=None, order='totalvolume', limit=10):
    try:
        if request.method == 'GET':
            kwargs = {'opt': opt, 'debug': False }
            dbhandler = hisdb_tasks[opt](**kwargs)
            starttime = datetime(*map(int, [starttime[0:4], starttime[4:6], starttime[6:8]]))
            endtime = datetime(*map(int, [endtime[0:4], endtime[4:6], endtime[6:8]]))
            traderids = traderids.split(',') if traderids else []
            args = (starttime, endtime, [stockid], order, limit)
            stockitem = dbhandler.stock.query_raw(*args)
            args = (starttime, endtime, [stockid], traderids, 'stock', order, limit)
            traderitem = dbhandler.trader.query_raw(*args)
        return JSONResponse({'stockitem': stockitem, 'traderitem': traderitem})
    except:
        return HttpResponse(404)

#def get_histrader_list(request, opt, starttime, endtime, order='totalvolume', limit=100):
#    try:
#        if request
#    db = hisdb_tasks[opt]()
#    id = iddb_tasks[opt]()
#    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
#    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
#    traderids = [id for id in id.trader.get_ids()]
#    args = (starttime, endtime, [], traderids, 'trader', order, limit)
#    traderitem = db.trader.query_raw(*args)
#    return render(request,'handler/histrader_list.html', {'traderitem': traderitem})
##    except:
##        404
#
#def histrader_detail(request, opt, traderid, starttime, endtime, stockids=None, order='totalvolume', limit=10):
#    db = hisdb_tasks[opt]()
#    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
#    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
#    stockids = stockids.split(',') if stockids else []
#    args = (starttime, endtime, stockids, [traderid], 'trader', order, limit)
#    traderitem = db.trader.query_raw(*args)
#    stockids = [it['stockid'] for it in traderitem]
#    args = (starttime, endtime, stockids, order, limit)
#    stockitem = db.stock.query_raw(*args)
#    return render(request,'handler/histrader_detail.html', {'stockitem': stockitem, 'traderitem': traderitem})
#
#
#def histrader_group(request, opt, starttime, endtime, order='totalvolume', limit=10):
#    db = hisdb_tasks[opt]()
#    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
#    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
#    groupitem = []
#    for i,it in enumerate(tradergroup):
#        traderids = it['groupids']
#        args = (starttime, endtime, [], traderids, 'trader', order, limit)
#        traderitem = db.trader.query_raw(*args)
#        groupitem.append({
#            'index': i,
#            'groupnm': it['groupnm'],
#            'traderitem': traderitem
#        })
#    return render(request,'handler/histrader_group.html', {'groupitem': groupitem})
#
##
#def hisstock_group(request, opt, starttime, endtime, order='totalvolume', limit=10):
#    db = hisdb_tasks[opt]()
#    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
#    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
#    groupitem = []
#    for i,it in enumerate(stockgroup):
#        stockids = it['groupids']
#        args = (starttime, endtime, stockids, [], 'stock', order, limit)
#        stockitem = db.trader.query_raw(*args)
#        groupitem.append({
#            'index': i,
#            'groupnm': it['groupnm'],
#            'stockitem': stockitem
#        })
#    return render(request,'handler/hisstock_group.html', {'groupitem': groupitem})
