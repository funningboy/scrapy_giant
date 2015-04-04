# -*- coding: utf-8 -*-

from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.tasks import query_hisstock, query_histoptrader
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler


#def dualema_list(request, hisdb,)
#
#def dualema_detail(request, hisdb, stockid, starttime, endtime, traderids=[], order='totalvolume', limit=10):
#    dbhandler = hisdb_tasks[hisdb]()
#    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
#    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
#    dd = endtime - starttime
#    maxlen = 30
#    if dd.days < maxlen:
#        return
#    args = (starttime, endtime, [stockid], order, limit)
#    data = dbhandler.transform_all_data(starttime, endtime, [stockid], traderids, order, limit)
#    if len(data[stockid].index) < maxlen:
#        return
#    dualema = DualEMAAlgorithm(dbhandler=dbhandler)
#    results = dualema.run(data).fillna(0)
#    report.collect(stockid, results)
#
#    if report.report.empty:
#        return
#
#    stream = report.iter_report(stockid, dtype='json')
#    render(request, 'reportitem')
#
#def
#
