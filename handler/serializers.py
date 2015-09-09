# -*- coding: utf-8 -*-

from main.views import create_search_collect
from main.routers import is_hisstock_list, is_hisstock_detail, is_histrader_list, is_histrader_detail
from main.serializers import *
from routers.tasks import *

@json_export
def hisstock_list_json(request):
    if request.method == 'GET':
        collect = create_search_collect(request)
        data = schedule_router_tasks(**collect)
        return JSONResponse(data)

@json_export
def hisstock_detail_json(request):
    if request.method == 'GET':
        collect = create_search_collect(request)
        data = schedule_router_tasks(**collect)
        return JSONResponse(data)

# debug
@json_export
def histrader_list_json(request):
    if request.method == 'GET':
        collect = create_search_collect(request)
        data = schedule_router_tasks(**collect)
        return JSONResponse(data)

@json_export
def histrader_detail_json(request):
    if request.method == 'GET':
        collect = create_search_collect(request)
        data = schedule_router_tasks(**collect)
        return JSONResponse(data)
