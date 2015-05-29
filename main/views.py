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
		'starttime': datetime.utcnow() - timedelta(days=100),
		'endtime': datetime.utcnow(),
		'stockids': [],
		'traderids': [],
		'algorithm': None
	}

	idhandler = {
		'twse': iddb_tasks['twse'](**kwargs),
		'otc': iddb_tasks['otc'](**kwargs)
	}

	# register router search table
	is_hisstock_detail: hisstock_detail_html(**cmds),
	is_hisstock_list: hisstock_list_html
	is_histrader_detail
	is_histrader_list
	is


def update(request, **cmd):
	if 'starttime' in request.GET and request.GET['starttime']:
       	cmds.update('starttime', datetime(*map(int, request.GET['starttime'].split('/'))))
    if 'endtime' in request.GET and request.GET['endtime']:
       	cmds.update('endtime', datetime(*map(int, request.GET['endtime'].split('/'))))
    if 'stockids' in request.GET and request.GET['stockids']:
       	cmds.update('stockids', set(request.GET['stockids'].split(',')))
    if 'traderids' in request.GET and request.GET['traderids']:
       	cmds.update('traderids', set(request.GET['traderids'].split(',')))
    if 'algorithm' in request.GET and request.GET['algorithm']:
       	cmds.update('algorithm', request.GET['algorithm'])
    
    # update stockids
    visit = []
    for sid in cmds['stockids']:
       	visit.append([
    		(idhandler['twse'].stock.has_id(sid), sid),
    		(idhandler['otc'].stock.has_id(sid), sid)
    	])
    twse, otc = zip(*visit)
    twse, otc = zip(*twse), zip(*otc)
    if twse and sum(twse[0]):
    	cmds.update({
    		'opt': 'twse',
    		'stockids': [i for i in compress(twse[1], twse[0])] 
    	})
    elif otc and sum(otc[0]):
    	cmds.update({
    		'opt': 'otc',
    		'stockids': [i for i in compress(otc[1], otc[0])]
    }) 
    # update traderids
    visit = []
    for td in cmds['traderids']:
    	visit.append((idhandler['twse'].trader.has_id(tid), tid))
    trader = zip(*vist)
    if trader and sum(trader[0]):
    	cmds.update({
    		'traderids': [i for i in compress(trader[1], trader[0])]
    	})
    
    	'hisstock': {
            'starttime': datetime.utcnow() - timedelta(days=100),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'order': 'totalvolume',
            'limit': 10
        },
        # histrader frame collect
        'histrader': {
            'starttime': datetime.utcnow() - timedelta(days=10),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'traderids':[],
            'base': 'stock',
            'order': 'totalvolume',
            'limit': 10
        },
        # hiscredit frame collect
        'hiscredit': {
            'starttime': datetime.utcnow() - timedelta(days=100),
            'endtime': datetime.utcnow(),
            'stockids': ['2317'],
            'order': 'decfinance',
            'limit': 10
        }	

    def is_hisstock_detail(request, **cmd):
    	if cmds['algorithm'] not in ['StockProfile0', 'StockProfile1', 'StockProfile2']:
    		return False
    	if cmds['starttime'] >= cmds['endtime'] or len(cmds['stockids']) != 1:
    		return False
    	return True

    def is_hisstock_list():
    	if cmds[algorithm] not in []:
    		return False
    	if cmds['starttime'] >= cmds['endtime']:
    		return False
    	cmds.update
    	return True

	def is_histrader_detail():
		if cmds['algorithm']
		pass

	def is_histrader_list():
		pass


