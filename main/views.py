# -*- coding: utf-8 -*-

from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from main.forms import FormTestItem

from handler.tasks import *

def home(request):
    stockids = None
    starttime = None
    endtime = None

    if 'stockids' in request.GET and request.GET['stockids']:
        stockids = request.GET['stockids'].split(',')

    if 'starttime' in request.GET and request.GET['starttime']:
        starttime = datetime(*map(int, request.GET['starttime'].split('/')))

    if 'endtime' in request.GET and request.GET['endtime']:
        endtime = datetime(*map(int, request.GET['endtime'].split('/')))

    if stockids and starttime and endtime:
        db = hisdb_tasks['twse']()
        args = (starttime, endtime, stockids, 'totalvolume', 10)
        stockitem = db.stock.query_raw(*args)
        args = (starttime, endtime, stockids, [], 'stock', 'totalvolume', 10)
        traderitem = db.trader.query_raw(*args)
        return render(request,'handler/hisstock_detail.html', {'stockitem': stockitem, 'traderitem': traderitem})
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.htm')


def search(request):
    if request.method == 'GET':
        pass
#        form = FormTestItem(request.GET)
#        form.save()
    return render(request, 'test.html')
