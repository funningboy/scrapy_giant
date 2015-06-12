# -*- coding: utf-8 -*-

import json
from bson import json_util
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from main.views import default_search
from main.tasks import *
from handler.tasks import collect_hisitem

# @
def hisstock_list_json(request):
    if request.method == 'GET':
        collect = default_search(request)
        if is_hisstock_list(**collect):
            data, _ = collect_hisitem(**collect)
            return JSONResponse(data)

#@
def hisstock_detail_json(request):
    if request.method == 'GET':
        collect = default_search(request)
        if is_hisstock_detail(**collect):
            data, _ = collect_hisitem(**collect)
            return JSONResponse(data)

def histrader_list_json(request):
    if request.method == 'GET':
        collect = default_search(request)
        if is_histrader_list(**collect):
            data, _ = collect_hisitem(**collect)
            return JSONResponse(data)

def histrader_detail_json(request):
    if request.method == 'GET':
        collect = default_search(request)
        if is_histrader_detail(**collect):
            data, _ = collect_hisitem(**collect)
            return JSONResponse(data)
