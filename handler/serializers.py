# -*- coding: utf-8 -*-

import json
from bson import json_util
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from main.views import default_search
from main.tasks import *
from handler.tasks import collect_hisitem

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# @
# @csrf_token
@api_view(['GET'])
def hisstock_list_json(request):
    if request.method == 'GET':
        collect = default_search(request)
        if is_hisstock_list(**collect):
            data, _ = collect_hisitem(**collect)
            return JSONResponse(data)

# @
@api_view(['GET'])
def hisstock_detail_json(request):
    if request.method == 'GET':
        collect = default_search(request)
        if is_hisstock_detail(**collect):
            data, _ = collect_hisitem(**collect)
            return JSONResponse(data)

@api_view(['GET'])
def histrader_list_json(request):
    if request.method == 'GET':
        collect = default_search(request)
        if is_histrader_list(**collect):
            data, _ = collect_hisitem(**collect)
            return JSONResponse(data)

@api_view(['GET'])
def histrader_detail_json(request):
    if request.method == 'GET':
        collect = default_search(request)
        if is_histrader_detail(**collect):
            data, _ = collect_hisitem(**collect)
            return JSONResponse(data)
