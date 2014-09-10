from django.conf.urls import patterns, include, url
from django.contrib import admin

from diverts import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flightplan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^$', views.index),
    url(r'^diverts/', include('diverts.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
