# -*- coding: utf-8 -*-

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET'])
def hisstock_list_json():
    try:
        if request.method == 'GET':
            return JSONResponse(data)
    except:
        return HttpResponse(404)

@api_view(['GET'])
def hisstock_detail_json(request):
    try:
        if request.method == 'GET':
            return JSONResponse(data)
    except:
        return HttpResponse(404)


##def histrader_group(request, opt, starttime, endtime, order='totalvolume', limit=10):
#    db = hisdb_tasks[opt]()
#    groupitem = []
#    for i,it in enumerate(tradergroup):
#        traderids = it['groupids']
#        args = (starttime, endtime, [], traderids, 'trader', order, limit)
#        traderitem = db.trader.query_raw(*args)
#        groupitem.append({
#            'index': i,
#            'groupnm': it['groupnm'],
#            'traderitem': traderitem
#        })
#    return render(request,'handler/histrader_group.html', {'groupitem': groupitem})
#
##
#def hisstock_group(request, opt, starttime, endtime, order='totalvolume', limit=10):
#    db = hisdb_tasks[opt]()
#    groupitem = []
#    for i,it in enumerate(stockgroup):
#        stockids = it['groupids']
#        args = (starttime, endtime, stockids, [], 'stock', order, limit)
#        stockitem = db.trader.query_raw(*args)
#        groupitem.append({
#            'index': i,
#            'groupnm': it['groupnm'],
#            'stockitem': stockitem
#        })
#    return render(request,'handler/hisstock_group.html', {'groupitem': groupitem})
