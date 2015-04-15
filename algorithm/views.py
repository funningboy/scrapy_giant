# -*- coding: utf-8 -*-

from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.tasks import query_hisstock, query_histoptrader
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler


def algorithm_list(request, opt, alg, starttime, endtime, limit=50):
    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
    args = (opt, alg, starttime, endtime, limit)
    run_algorithm_service.delay(*args).get()

def dualema_detail(request, opt, stockid, starttime, endtime, traderids=[], order='totalvolume', limit=10):


def dualema_detail
def besttrader_detail
