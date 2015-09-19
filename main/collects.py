# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.conf import settings

def create_search_collect(request):
    starttime = datetime.utcnow() - timedelta(days=150)
    endtime = datetime.utcnow()
    stockids = []
    traderids = []
    opt = None
    algorithm = None

    # form.is_valid
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

    collect = {
        'starttime': starttime,
        'endtime': endtime,
        'stockids': stockids,
        'traderids': traderids,
        'opt': opt,
        'algorithm': algorithm,
        'debug': settings.DEBUG
    }
    return collect


def create_autocmp_collect(request):
    opt = None

    if 'opt' in request.GET and request.GET['opt']:
        opt = request.GET['opt']

    collect = {
        'opt': opt
    }
    return collect