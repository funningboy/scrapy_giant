# -*- coding: utf-8 -*-

from mongoengine import *

class TestItem(Document):
    id = IntField(required=True)
    name = StringField(max_length=70, required=True)
    meta = {
        'db_alias': 'test',
        'allow_inheritance': True,
        'indexes': [('id', 'name')]
    }
