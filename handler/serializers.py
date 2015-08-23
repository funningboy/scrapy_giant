# -*- coding: utf-8 -*-

from main.views import create_search
from main.routers import is_hisstock_list, is_hisstock_detail, is_histrader_list, is_histrader_detail
from main.serializers import *
from routers.tasks import *

@json_export
def hisstock_list_json(request):
    pass

#@json_export
def hisstock_detail_json(request):
    if request.method == 'GET':
        collect = {
            'all_debug': True,
            'all_stockids': '["2317"]'
        }
        data = collect_hisstock_detail(**collect)
        return JSONResponse(data)

@json_export
def histrader_list_json(request):
    pass

@json_export
def histrader_detail_json(request):
    if request.method == 'GET':
        collect = {
            'all_debug': True,
            'all_traderids': '["1650"]',
        }
        data = collect_histrader_detail(**collect)
        return JSONResponse(data)
