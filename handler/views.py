# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render

from handler.tasks import *
from handler.group import *

def hisstock_list_html(request, **collect):
    try:
        if request.method == 'GET':
            return render(request, 'handler/hisstock_list.html', collect)
    except:
        return HttpResponse(404)

def hisstock_detail_html(request, **collect):
    try:
        if request.method == 'GET':
            return render(request, 'handler/hisstock_detail.html', collect)
    except:
        return HttpResponse(404)

