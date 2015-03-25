# -*- coding: utf-8 -*-

from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from handler.tasks import query_hisstock, query_histoptrader
from handler.iddb_handler import TwseIdDBHandler, OtcIdDBHandler



