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
    ),
    url(r'^api/histrader_detail/',
        view=serializers.histrader_detail_json,
        name='histrader_detail_json'
    ),
    url(r'^api/histrader_list/',
        view=serializers.histrader_list_json,
        name='histrader_list_json'
    ),
    url(r'^api/allid_list/',
        view=serializers.allid_list_json,
        name='allid_list_json'
    )
)
