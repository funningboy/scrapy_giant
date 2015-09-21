# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.views import *
from main.collects import *
from main.routers import *

routers = (
    (is_hisstock_detail, hisstock_detail_html),
    (is_histrader_detail, histrader_detail_html),
    (is_teststock_detail, hisstock_detail_html),
    (is_testtrader_detail, histrader_detail_html),
    (is_hisstock_list, hisstock_list_html),
    (is_histrader_list, histrader_list_html),
    (is_teststock_list, hisstock_list_html),
    (is_testtrader_list, histrader_list_html)
)

def home(request):
    return render(request, 'main/home.html', {})

def about(request):
    return render(request, 'main/about.html', {})

def error_search(request):
    return render(request, 'main/error_search.html', {})

def router_search(request):
    collect = create_search_collect(request)
    for r in routers:
        if r[0](collect):
            return r[1](request, collect) 
    return error_search(request)