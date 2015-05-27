
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^main/', 'main.views.search', name='search'),
    url(r'^test/', 'main.views.test', name='test'),
    url(r'^about/$', 'main.views.about', name='about'),
    url(r'^handler/', include('handler.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
