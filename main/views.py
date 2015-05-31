# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from main.forms import FormSearchItem

from handler.tasks import *

def home(request):
    form = FormSearchItem()
    return render(request, 'base.html', {'form': form})

def about(request):
    return render(request, 'about.htm')

def router_search(request):
    cmds = {
   }


def update(request):
    starttime = datetime.utcnow() - timedelta(days=100)
    endtime = datetime.utcnow()
    stockids = []
    traderids = []
    algorithm = None

    # populate
    if 'starttime' in request.GET and request.GET['starttime']:
        starttime = datetime(*map(int, request.GET['starttime'].split('/')))
    if 'endtime' in request.GET and request.GET['endtime']:
        endtime = datetime(*map(int, request.GET['endtime'].split('/')))
    if 'stockids' in request.GET and request.GET['stockids']:
        stockids =  set(request.GET['stockids'].split(','))
    if 'traderids' in request.GET and request.GET['traderids']:
        traderids = set(request.GET['traderids'].split(','))
    if 'algorithm' in request.GET and request.GET['algorithm']:
        algorithm = request.GET['algorithm']

    cmd = {
        'starttime': starttime,
        'endtime': endtime,
        'stockids': stockids,
        'traderids': traderids,
        'algorithm': algorithm,
        'opt': opt
    }
    return cmd
