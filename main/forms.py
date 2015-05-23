# -*- coding: utf-8 -*-

from mongodbforms import DocumentForm
from main.models import TestItem

class FormTestItem(DocumentForm):
    meta = {
        'document': TestItem,
        'fields': ('id', 'name')
    }
