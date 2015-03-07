# -*- coding: utf-8 -*-

from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.tasks import query_hisstock, query_histoptrader
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler


#def superman_detail(request, hisdb, starttime, endtime, )
#    idhandler = iddb_tasks[hisdb]()
#    start_yy, start_mm, start_dd = int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8])
#    end_yy, end_mm, end_dd = int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8])
#    starttime, endtime = datetime(start_yy, start_mm, start_dd), datetime(end_yy, end_mm, end_dd)
#    stockids =[id for id in idhandler.stock.get_ids()]
#
#def superman_list
#
#def darkman_detail(request, hisdb, starttime, endtime, )
