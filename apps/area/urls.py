__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.area import views

urlpatterns = patterns('',
                       url(r'^area$', views.AreaView.as_view()),
                       )
