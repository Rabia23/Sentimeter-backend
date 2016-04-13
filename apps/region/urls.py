__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.region import views

urlpatterns = patterns('',
                       url(r'^region$', views.RegionView.as_view()),
                       )
