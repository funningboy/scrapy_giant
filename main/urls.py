# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

# rest framework url
#router = routers.DefaultRouter()
#router.register(r'legislator', views.LegislatorViewSet)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^about/$', 'main.views.about', name='about'),
    url(r'^router_search/$', 'main.views.router_search', name='router_search'),
    url(r'^handler/', include('handler.urls')),
    url(r'^algorithm/', include('algorithm.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
