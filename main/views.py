# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render

from giant.settings import _debug
from handler.tasks import *
from handler.views import *
from handler.table import default_hiscollect
from main.tasks import *
from main.table import *

#
def home(request):
    if request.method == 'GET':
        tags = home_tags()
        return render(request, 'base.html', tags)

def about(request):
    pass

# @
def router_search(request):
    if request.method == 'GET':
        collect = default_search(request)
        router = [
            # query
            (is_hisstock_detail, hisstock_detail_html),
            #(is_histrader_detail, histrader_detail_html),
            #(is_dualema_detail, dualema_detail_html),
            #(is_btrader_detail, btader_detail_html),
            #(is_bbands_detail, bbands_detail_html),
            # alg
            (is_hisstock_list, hisstock_list_html)
            #(is_histrader_list, histrader_list_html),
        ]
        for r in router:
            if (r[0](**collect)):
                return r[1](request, **collect)
        return home(request)
#
def router_portfolio(request):
    collect = default_portfolio(request)
    router = [
        #(is_dualema_list, dualema_list_html),
        #(is_btrader_list, btader_list_html),
        #(is_bbands_list, bbands_list_html)
    ]
    for r in router:
        if r[0](**collect):
            return r[1](request, **collect)
    return home(request)

def default_search(request):
    starttime = datetime.utcnow() - timedelta(days=150)
    endtime = datetime.utcnow()
    stockids = []
    traderids = []
    opt = None
    algorithm = None

    if 'starttime' in request.GET and request.GET['starttime']:
        starttime = datetime(*map(int, request.GET['starttime'].split('/')))
    if 'endtime' in request.GET and request.GET['endtime']:
        endtime = datetime(*map(int, request.GET['endtime'].split('/')))
    if 'stockids' in request.GET and request.GET['stockids']:
        stockids =  list(set(request.GET['stockids'].split(',')))
    if 'traderids' in request.GET and request.GET['traderids']:
        traderids = list(set(request.GET['traderids'].split(',')))
    if 'opt' in request.GET and request.GET['opt']:
        opt = request.GET['opt']
    if 'algorithm' in request.GET and request.GET['algorithm']:
        algorithm = request.GET['algorithm']

    kwargs = {
        'starttime': starttime,
        'endtime': endtime,
        'stockids': stockids,
        'traderids': traderids,
        'opt': opt,
        'algorithm': algorithm,
        'debug': _debug
    }
    return default_hiscollect(**kwargs)

def default_portfolio(request):
    watchtime = datetime.utcnow()

    if 'watchtime' in request.GET and request.GET['watchtime']:
        watchtime = datetime(*map(int, request.GET['watchtime'].split('/')))

    kwargs = {}
    return default_hisprofolio(**kwargs)
