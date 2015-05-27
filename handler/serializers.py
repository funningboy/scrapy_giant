# -*- coding: utf-8 -*-

from rest_framework.renderers import JSONRenderer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view
def get_hisstock_list_json():
    try:
        if request.
            kwargs = {}
            dbhandler = hisdb_tasks[opt](**kwargs)
            kwargs = {}
            idhandler = iddb_tasks[opt](**kwargs)
            stockids = set([id for id in idhandler.stock.get_ids()])
            args = (starttime, endtime, stockids, order, limit)
            stockitem = dbhandler.stock.query_raw(*args)
            nstockids =
            args = (starttime, endtime, )
            data = {'stockitem': }
            return render(request, 'handler/hisstock_list.html')
    except:
        return HttpResponse(404)

@api_view(['GET'])
def get_hisstock_detail_json(request):
    try:
        if request.method == 'GET':
            unpackage(request.)
            kwargs = {'opt': opt, 'debug': False }
            dbhandler = hisdb_tasks[opt](**kwargs)
            traderids = set(traderids.split(',') if traderids else [])
            args = (starttime, endtime, [stockid], stock_order, limit)
            stockitem = dbhandler.stock.query_raw(*args)
            args = (starttime, endtime, [stockid], traderids, 'stock', trader_order, limit)
            traderitem = dbhandler.trader.query_raw(*args)
            args = (starttime, endtime, [stockid], credit_order, limit)
            credititem = dbhandler.credit.query_raw(*args)
            data = {'stockitem': stockitem, 'traderitem': traderitem, 'credititem': credititem}
            return JSONResponse(data)
    except:
        return HttpResponse(404)

@api_view
#def histrader_detail(request, opt, traderid, starttime, endtime, stockids=None, order='totalvolume', limit=10):
#    db = hisdb_tasks[opt]()
#    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
#    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
#    stockids = stockids.split(',') if stockids else []
#    args = (starttime, endtime, stockids, [traderid], 'trader', order, limit)
#    traderitem = db.trader.query_raw(*args)
#    stockids = [it['stockid'] for it in traderitem]
#    args = (starttime, endtime, stockids, order, limit)
#    stockitem = db.stock.query_raw(*args)
#    return render(request,'handler/histrader_detail.html', {'stockitem': stockitem, 'traderitem': traderitem})


##def histrader_group(request, opt, starttime, endtime, order='totalvolume', limit=10):
#    db = hisdb_tasks[opt]()
#    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
#    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
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
#    starttime = datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
#    endtime = datetime(int(endtime[0:4]), int(endtime[4:6]), int(endtime[6:8]))
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
