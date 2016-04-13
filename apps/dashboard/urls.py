__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.dashboard import views

urlpatterns = patterns('',
                       url(r'^data_view$', views.DataView.as_view()),
                       url(r'^socket_test$', views.SocketTest.as_view()),
                       )
