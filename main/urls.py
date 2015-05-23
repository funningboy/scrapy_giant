
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^about/$', 'main.views.about', name='about'),
    url(r'handler/', include('handler.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
