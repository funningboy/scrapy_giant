# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

# rest framework url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', view='main.views.home', name='home'),
    url(r'^about/$', view='main.views.about', name='about'),
    url(r'^routers/', include('routers.urls')),
    url(r'^handler/', include('handler.urls')),
    url(r'^algorithm/', include('algorithm.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
