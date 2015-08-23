# -*- coding: utf-8 -*-

from mongoengine import *
from mongodbforms import DocumentForm
from main.models import SearchItem

class FormSearchItem(DocumentForm):
    class Meta:
        document = SearchItem
        fields = ['opt', 'starttime','endtime', 'stockids', 'traderids', 'algorithm']
