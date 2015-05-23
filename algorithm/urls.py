# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from algorithm import views

urlpatterns = patterns('',

    # ex: /algorithm/dualema/twse/20140808/20141111/2317
    # ex: /algorithm/dualema/otc/20140808/20141111/5371
    url(r'^dualema/(?P<opt>\w+)/(?P<starttime>\d{8})/(?P<endtime>\d{8})/$',
        view=views.dualema_detail,
        name='dualema_detail'
    ),

    # ex: /algorithm/dualema/twse/20141111
    # ex: /algorithm/dualema/otc/20141111
    url(r'^(?P<alg>\w+)/(?P<opt>\w+)/(?P<endtime>\d{8})/$',
        view=views.dualema_list,
        name='dualema_list'
    )
)



