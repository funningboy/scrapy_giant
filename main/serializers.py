# -*- coding: utf-8 -*-

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def json_export(function):
    def wrap(request, **kwargs):
        try:
            return function(request, **kwargs)
        except:
            return HttpResponse(404)
    return wrap
