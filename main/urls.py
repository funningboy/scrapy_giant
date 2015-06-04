
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^router_search/', 'main.views.router_search', name='router_search'),
    url(r'^router_portfolio/', 'main.views.router_portfolio', name='router_portfolio'),
    url(r'^about/$', 'main.views.about', name='about'),
    url(r'^handler/', include('handler.urls')),
    url(r'^algorithm/', include('algorithm.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
