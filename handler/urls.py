# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from handler import views

urlpatterns = patterns('',
    # ex: /handler/twse/2317/20140808/20141111
#    url(r'^twse/(?P<stockid>\w+)/(?<starttime>\d{8})/(?<endtime>\d{8})/$',
#        view=views.hisstock_detail,
#        name='hisstock_detail'
#    ),
    url(r'^$',
        view=views.hisstock_list,
        name='hisstock_list'
    )
)
