# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.views import *
from main.collects import *
from main.routers import *

#
def home(request):
    return render(request, 'main/home.html', {})

def about(request):
    return render(request, 'main/about.html', {})

# @
def router_search(request):
    collect = create_search(request)
    routers = [
        # detail query
        (is_hisstock_detail, hisstock_detail_html),
        (is_histrader_detail, histrader_detail_html),
        #(is_dualema_detail, dualema_detail_html),
        #(is_btrader_detail, btader_detail_html),
        #(is_bbands_detail, bbands_detail_html),
        # list query
        (is_hisstock_list, hisstock_list_html),
        (is_histrader_list, histrader_list_html),
    ]
    for r in router:
        if r[0](collect):
            return r[1](request, collect)
    return home(request)
#
def router_portfolio(request):
    collect = create_portfolio(request)
    routers = [
        #(is_dualema_list, dualema_list_html),
        #(is_btrader_list, btader_list_html),
        #(is_bbands_list, bbands_list_html)
    ]
    for r in router:
        if r[0](collect):
            return r[1](request, collect)
    return home(request)

