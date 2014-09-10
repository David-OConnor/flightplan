from django.conf.urls import patterns, url
from diverts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)

#todo remove autodiscover from squadron (project level) urls.py once you upg to 1.7