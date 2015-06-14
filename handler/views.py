# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def hisstock_list_html(request, collect):
	return render(request, 'handler/hisstock_list.html', collect)

@csrf_protect
def hisstock_detail_html(request, collect):
    return render(request, 'handler/hisstock_detail.html', collect)

@csrf_protect
def histrader_list_html(request, collect):
    return render(request, 'handler/histrader_list.html', collect)

@csrf_protect
def histrader_detail_html(request, collect):
    return render(request, 'handler/histrader_detail.html', collect)
