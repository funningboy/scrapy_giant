# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def hisstock_list_html(request, **collect):
    if request.method == 'GET':
        tags = hisstock_list_tags(**collect)
        return render(request, 'handler/hisstock_list.html', tags)

@csrf_protect
def hisstock_detail_html(request, **collect):
    if request.method == 'GET':
        tags = hisstock_detail_tags(**collect)
        return render(request, 'handler/hisstock_detail.html', tags)

@csrf_protect
def histrader_list_html(request, **collect):
    if request.method == 'GET':
        tags = histrader_list_tags(**collect)
        return render(request, 'handler/histrader_list_html', tags)

@csrf_protect
def histrader_detail_html(request, **collect):
    if request.method == 'GET':
        tags = histrader_detal_tags(**collect)
        return render(request, 'handler/histrader_detail_html', tags)
