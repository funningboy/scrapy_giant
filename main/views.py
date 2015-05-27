# -*- coding: utf-8 -*-

from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from main.forms import FormSearchItem

from handler.tasks import *

def home(request):
    form = FormSearchItem()
    return render(request, 'base.html', {'form': form})

def about(request):
    return render(request, 'about.htm')

def test(request):
    form = FormTestItem()
    return render(request, 'test.html', {'form': form})

#def search(request):
#    params = {
#        'starttime': None,
#        'endtime': None,
#        'stockids': [],
#        'traderids': [],
#        'algorithm': None,
#        'base': None
#    }
#
#    if request.method == 'GET':
#
#def populate_search(params):
#    if 'starttime' in request.GET and request.GET['starttime']:
#        params.update('starttime', datetime(*map(int, request.GET['starttime'].split('/'))))
#
#    if 'endtime' in request.GET and request.GET['endtime']:
#        params.update('endtime', datetime(*map(int, request.GET['endtime'].split('/'))))
#
#    if 'stockids' in request.GET and request.GET['stockids']:
#        params.update('stockids', request.GET['stockids'].split(','))
#
#    if 'traderids' in request.GET and request.GET['traderids']:
#        params.update('traderids', request.GET['traderids'].split(','))
#
#    if 'algorithm' in request.GET and request.GET['algorithm']:
#        params.update('algorithm', request.GET['algorithm'])
#
#    if 'base' in request.GET and request.GET['base']:
#        params.update('base': request.GET['base'])
#
#
#def is_hisstock_detail(**params):
#    if params['starttime'] <= params['endtime'] and params['algorithm'] == 'stockdetail' and len(params['stockids']) == 1:
#        if iddb_tasks['twse'](debug=).stock.has_id(params['stockids'][0]):
#            opt = 'twse'
#        iddb_tasks['otc'](debug=).stock.has_id(params['stockids'][0]):
#            opt = 'otc'
#    get_hisstock_detail()
#
#def is_hisstock_list
#
#def is_histrader_detail
#
#def is_histrader_list

