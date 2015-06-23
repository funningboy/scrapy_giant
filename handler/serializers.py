# -*- coding: utf-8 -*-

from main.views import create_search
from main.routers import is_hisstock_list, is_hisstock_detail, is_histrader_list, is_histrader_detail
from main.serializers import *
from handler.tasks import collect_hisitem

@json_export
def hisstock_list_json(request):
    if request.method == 'GET':
        collect = create_search(request)
        if is_hisstock_list(collect):
            data, _ = collect_hisitem(collect)
            return JSONResponse(data)

@json_export
def hisstock_detail_json(request):
    if request.method == 'GET':
        collect = create_search(request)
        if is_hisstock_detail(collect):
            data, _ = collect_hisitem(collect)
            return JSONResponse(data)

@json_export
def histrader_list_json(request):
    if request.method == 'GET':
        collect = create_search(request)
        if is_histrader_list(collect):
            data, _ = collect_hisitem(collect)
            return JSONResponse(data)

@json_export
def histrader_detail_json(request):
    if request.method == 'GET':
        collect = create_search(request)
        if is_histrader_detail(collect):
            data, _ = collect_hisitem(collect)
            return JSONResponse(data)
