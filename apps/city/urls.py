__author__ = 'aamish'

from django.conf.urls import patterns, url
from apps.city import views

urlpatterns = patterns('',
                       url(r'^city$', views.CityView.as_view()),
                       )
