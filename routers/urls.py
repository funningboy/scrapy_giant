# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from routers import views


urlpatterns = patterns('',
    url(r'^index/$',
        view='routers.views.index',
        name='routers_index'
    )
)