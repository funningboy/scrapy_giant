# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from handler import views
from handler import serializers

urlpatterns = patterns('',
    url(r'^api/hisstock_detail/',
        view=serializers.hisstock_detail_json,
        name='hisstock_detail_json'
    ),
    url(r'^api/hisstock_list/',
        view=serializers.hisstock_list_json,
        name='hisstock_list_json'
    )
)
