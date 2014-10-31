from django.conf.urls import patterns, include, url
from django.contrib import admin

from demoapp.views import MyView

urlpatterns = patterns('',
    # Examples:
     url(r'^$', MyView.as_view(), name='view'),
    # url(r'^demoapp/', include('blog.urls')),
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^proj/', include('proj.foo.urls')),
    #url(r'^admin/', include(admin.site.urls)),
)
