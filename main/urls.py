
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'handler/', include('handler.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
