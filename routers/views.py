 #-*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render


def index(request):
    return render(request, 'routers/index.html', {})
