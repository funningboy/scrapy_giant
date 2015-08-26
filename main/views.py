# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.views import *
from main.collects import *
from main.routers import *

def home(request):
    return render(request, 'main/home.html', {})

def about(request):
    return render(request, 'main/about.html', {})

def router_search(request):
    collect = create_search(request)
    #return hisstock_detail_html(request, collect)
    #return histrader_detail_html(request, collect)
    return hisstock_list_html(request, collect)
    #return histrader_list.html(request, collect)
    return home(request)


