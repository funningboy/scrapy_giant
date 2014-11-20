# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.models import TwseHisColl, OtcHisColl
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler
from handler.hisdb_handler import TwseHisDBHandler, OtcHisDBHandler

hisdb_tasks = {
    'twse': TwseHisDBHandler,
    'otc': OtcHisDBHandler
}

def hisstock_list(request):
    return render(request,'handler/stockAddRemovePanel.html')


def hisstock_detail(request, hisdb, starttime, endtime, stockids=[]):
#    try:
#        dbhandler = hisdb_tasks[hisdb]()
#        dbhandler.stock.ids = stockids
#        cursor = dbhandler.stock.query(
#            starttime=starttime,
#            endtime=endtime,
#            stockids=stockids)
#    except Exception, e:
#        print e
#        return HttpResponseRedirect('/')
    return render(request,'handler/stockAddRemovePanel.html', {'item': cursor})
