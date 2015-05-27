# -*- coding: utf-8 -*-

from mongodbforms import DocumentForm
from mongoengine import *
from main.models import SearchItem

class FormSearchItem(DocumentForm):
    class Meta:
        document = SearchItem
        fields = ['starttime','endtime', 'stockids', 'traderids', 'algorithm']
