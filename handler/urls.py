# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from handler import views

urlpatterns = patterns('',
    #  /handler/hisstock/twse

    # ex: /handler/hisstock/twse/2317/20140808/20141111
    url(r'^hisstock/(?P<hisdb>\w+)/(?P<stockid>\w+)/(?P<starttime>\d{8})/(?P<endtime>\d{8})/$',
        view=views.hisstock_detail,
        name='hisstock_detail'
    ),
    # ex: /handler/hisstock/otc/5371/20140808/20141111
    url(r'^hisstock/(?P<hisdb>\w+)/(?P<stockid>\w+)/(?P<starttime>\d{8})/(?P<endtime>\d{8})/$',
        view=views.hisstock_detail,
        name='hisstock_detail'
    ),
    # ex: /handler/hisstock/twse/2317/1440,1111//20140808/20141111
    url(r'^hisstock/(?P<hisdb>\w+)/(?P<stockid>\w+)/(?P<traderid>)/(?P<starttime>\d{8})/(?P<endtime>\d{8})/$',
        view=views.hisstock_detail,
        name='hisstock_detail'
    ),
    # ex: /handler/histrader/twse/1440/20140808/20141111
    url(r'^histrader/(?P<hisdb>\w+)/(?P<traderid>\w+)/(?P<starttime>\d{8})/(?P<endtime>\d{8})/$',
        view=views.histrader_detail,
        name='histrader_detail'
    ),
    # ex: /handler/histrader/all/1440/20140808/20141111
    # ex: /hand;er/histrader/otc/1440/20140808/20141111

    # ex: /handler/histrader/twse/1470/20140808/20141111
    url(r'^$',
        view=views.hisstock_list,
        name='hisstock_list'
    )
)
